import logging
import os
import re
from collections import defaultdict
from enum import Enum, auto
from textwrap import dedent

import jellyfish
import numpy as np
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import nltk

from courses.course_text_heuristics import title_heuristics, description_heuristics

from courses.models import Topic
from PennCourses.settings.base import S3_client


def get_branches_from_cross_walk(cross_walk):
    """
    From a given crosswalk csv path, generate a dict mapping old_full_code to
    a list of the new codes originating from that source, if there are multiple
    (i.e. only in the case of branches).
    """
    branched_links = defaultdict(list)
    cross_walk = pd.read_csv(cross_walk, delimiter="|", encoding="unicode_escape")
    for _, r in cross_walk.iterrows():
        old_full_code = f"{r['SRS_SUBJ_CODE']}-{r['SRS_COURSE_NUMBER']}"
        new_full_code = f"{r['NGSS_SUBJECT']}-{r['NGSS_COURSE_NUMBER']}"
        branched_links[old_full_code].append(new_full_code)
    return {
        old_code: new_codes for old_code, new_codes in branched_links.items() if len(new_codes) > 1
    }


MODEL = SentenceTransformer("all-MiniLM-L6-v2")
nltk.download('punkt')


def get_direct_backlinks_from_cross_walk(cross_walk):
    """
    From a given crosswalk csv path, generate a dict mapping new_full_code->old_full_code,
    ignoring branched links in the crosswalk (a course splitting into multiple new courses).
    """
    links = defaultdict(list)
    cross_walk = pd.read_csv(cross_walk, delimiter="|", encoding="unicode_escape")
    for _, r in cross_walk.iterrows():
        old_full_code = f"{r['SRS_SUBJ_CODE']}-{r['SRS_COURSE_NUMBER']}"
        new_full_code = f"{r['NGSS_SUBJECT']}-{r['NGSS_COURSE_NUMBER']}"
        links[old_full_code].append(new_full_code)
    return {old_code: new_codes[0] for old_code, new_codes in links.items() if len(new_codes) == 1}


def prompt_for_link_multiple(courses, extra_newlines=True):
    """
    Prompts the user to confirm or reject a possible link between multiple courses.
    Returns a boolean representing whether the courses should be linked.
    """
    print("\n\n============>\n")
    print("\n".join(course.full_str() for course in courses))
    print("\n<============")
    prompt = input(f"Should the above {len(courses)} courses be linked? (y/N) ")
    if extra_newlines:
        print("\n\n")
    return prompt.strip().upper() == "Y"


def prompt_for_link(course1, course2):
    """
    Prompts the user to confirm or reject a possible link between courses.
    Returns a boolean representing whether the courses should be linked.
    """
    return prompt_for_link_multiple([course1, course2])


def same_course(course_a, course_b):
    return course_a.full_code == course_b.full_code or any(
        course_ac.full_code == course_b.full_code
        for course_ac in (course_a.primary_listing or course_a).listing_set.all()
    )


class ShouldLinkCoursesResponse(Enum):
    DEFINITELY = auto()
    MAYBE = auto()
    NO = auto()


def should_link_courses(course_a, course_b, verbose=True):
    """
    Checks if the two courses should be linked, based on information about those
    courses stored in our database. Prompts for user input in the case of possible links,
    if in verbose mode (otherwise just logs possible links).
    Returns a response in the form of a ShouldLinkCoursesResponse enum.
    """
    if same_course(course_a, course_b):
        return ShouldLinkCoursesResponse.DEFINITELY
    elif course_a.semester == course_b.semester:
        return ShouldLinkCoursesResponse.NO
    elif (course_a.code < "5000") != (course_b.code < "5000"):
        return ShouldLinkCoursesResponse.NO
    elif similar_courses(course_a, course_b):
        # If title is same or (title is similar and description is similar
        # have a fairly low threshold for similarity)
        if verbose and prompt_for_link(course_a, course_b):
            return ShouldLinkCoursesResponse.DEFINITELY
        if not verbose:
            # Log possible link
            logging.info(f"Found possible link between {course_a} and {course_b}")
        return ShouldLinkCoursesResponse.MAYBE
    return ShouldLinkCoursesResponse.NO


def lev_divided_by_avg_title_length(title1, title2):
    """
    Compute levenshtein distance between 2 titles and then divide by avg title length.
    """
    if title1 is np.NaN or title2 is np.NaN:
        return 0.0
    return 2 * jellyfish.levenshtein_distance(title1, title2) / (len(title1) + len(title2))


def semantic_similarity(string_a, string_b):
    """
    Compute the semantics similarity between two
    strings. The strings are split into sentences, then
    those sentences are turned into embeddings, and then
    cosine similarity between matching sentences is computed.
    If the two strings have different numbers of sentences,
    take the maximum similarity matching that contains
    as many sentences as possible.
    """
    string_a = string_a.strip().lower()
    string_b = string_b.strip().lower()
    sentences_a = nltk.tokenize.sent_tokenize(string_a)
    sentences_b = nltk.tokenize.sent_tokenize(string_b)
    emb_a = MODEL.encode(sentences_a, convert_to_tensor=True)
    emb_b = MODEL.encode(sentences_b, convert_to_tensor=True)
    cosine_scores = util.cos_sim(emb_a, emb_b)
    nrows, ncols = cosine_scores.shape
    # compute tr/len(diag) for maximal length diagonals
    max_trace = 0.0
    for offset in range(0, ncols - nrows + 1):  # [0, cols - rows]
        diag = np.diagonal(cosine_scores, offset=offset)
        max_trace = max(max_trace, np.sum(diag) / len(diag))
    return max_trace


def similar_courses(course_a, course_b):
    if lev_divided_by_avg_title_length(
        course_a.title, course_b.title
    ) > 0.8 and not title_heuristics(course_a.title, course_b.title):
        return True
    return (
        semantic_similarity(course_a.description, course_b.description) > 0.6
        and semantic_similarity(course_a.title, course_b.title) > 0.6
        and not description_heuristics(course_a.description, course_b.description)
    )


def merge_topics(guaranteed_links=None, verbose=False):
    """
    Finds and merges Topics that should be merged.
    Args:
        guaranteed_links: Optionally, a `guaranteed_links` dict returned by
            `get_direct_backlinks_from_cross_walk`.
        verbose: If verbose=True, this script will print its progress and prompt for user input
            upon finding possible (but not definite) links. Otherwise it will run silently and
            log found possible links to Sentry (more appropriate if this function is called
            from an automated cron job like registrarimport).
    """
    if verbose:
        print("Merging topics")
    guaranteed_links = guaranteed_links or dict()
    if verbose:
        print("Loading topics and courses from db (this may take a while)...")
    topics = set(
        Topic.objects.prefetch_related(
            "courses",
            "courses__listing_set",
            "courses__primary_listing",
            "courses__primary_listing__listing_set",
        ).all()
    )
    dont_link = set()
    merge_count = 0

    for topic in tqdm(list(topics), disable=(not verbose)):
        if topic not in topics:
            continue
        keep_linking = True
        while keep_linking:
            keep_linking = False
            for topic2 in topics:
                if topic == topic2:
                    continue
                merged_courses = list(topic.courses.all()) + list(topic2.courses.all())
                merged_courses.sort(key=lambda c: (c.semester, c.topic_id))
                course_links = []
                last = merged_courses[0]
                for course in merged_courses[1:]:
                    if last.topic_id != course.topic_id:
                        course_links.append((last, course))
                    last = course
                if any(
                    course_a.semester == course_b.semester and not same_course(course_a, course_b)
                    for course_a, course_b in course_links
                ):
                    continue
                should_link = True
                for last, course in course_links:
                    if (last, course) in dont_link or (
                        should_link_courses(last, course, verbose=verbose)
                        != ShouldLinkCoursesResponse.DEFINITELY
                    ):
                        dont_link.add((last, course))
                        should_link = False
                        break
                if should_link:
                    topics.remove(topic)
                    topics.remove(topic2)
                    topic = topic.merge_with(topic2)
                    topics.add(topic)
                    merge_count += 1
                    keep_linking = True
                    break

    if verbose:
        print(f"Finished merging topics (performed {merge_count} merges).")


def manual_merge(topic_ids):
    invalid_ids = [i for i in topic_ids if not i.isdigit()]
    if invalid_ids:
        print(
            f"The following topic IDs are invalid (non-integer):\n{invalid_ids}\n" "Aborting merge."
        )
        return
    topic_ids = [int(i) for i in topic_ids]
    topics = Topic.objects.filter(id__in=topic_ids).prefetch_related("courses")
    found_ids = topics.values_list("id", flat=True)
    not_found_ids = list(set(topic_ids) - set(found_ids))
    if not_found_ids:
        print(f"The following topic IDs were not found:\n{not_found_ids}\nAborting merge.")
        return
    courses = [course for topic in topics for course in topic.courses.all()]
    if not prompt_for_link_multiple(courses, extra_newlines=False):
        print("Aborting merge.")
        return
    with transaction.atomic():
        topic = topics[0]
        for topic2 in topics[1:]:
            topic = topic.merge_with(topic2)
    print(f"Successfully merged {len(topics)} topics into: {topic}.")


class Command(BaseCommand):
    help = (
        "This script uses a combination of an optionally provided crosswalk, heuristics, "
        "and user input to merge Topics in the database."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--cross-walk",
            type=str,
            help=dedent(
                """
                Optionally specify a path to a crosswalk specifying links between course codes
                (in the format provided by Susan Collins [squant@isc.upenn.edu] from
                the data warehouse team; https://bit.ly/3HtqPq3).
                """
            ),
            default="",
        )
        parser.add_argument(
            "-s3", "--s3_bucket", help="download crosswalk from specified s3 bucket."
        )
        parser.add_argument(
            "-t",
            "--topic_ids",
            nargs="*",
            help=dedent(
                """
            Optionally, specify a (space-separated) list of Topic IDs to merge into a single topic.
            You can find Topic IDs from the django admin interface (either by searching through
            Topics or by following the topic field from a course entry).
            If this argument is omitted, the script will automatically detect merge opportunities
            among all Topics, prompting the user for confirmation before merging in each case.
            """
            ),
            required=False,
        )

    def handle(self, *args, **kwargs):
        cross_walk_src = kwargs["cross_walk"]
        s3_bucket = kwargs["s3_bucket"]
        topic_ids = set(kwargs["topic_ids"])

        print(
            "This script is atomic, meaning either all Topic merges will be comitted to the "
            "database, or otherwise if an error is encountered, all changes will be rolled back "
            "and the database will remain as it was before the script was run."
        )

        if topic_ids:
            manual_merge(topic_ids)
            return

        if cross_walk_src and s3_bucket:
            fp = "/tmp/" + cross_walk_src
            print(f"downloading crosswalk from s3://{s3_bucket}/{cross_walk_src}")
            S3_client.download_file(s3_bucket, cross_walk_src, fp)
            cross_walk_src = fp

        guaranteed_links = (
            get_direct_backlinks_from_cross_walk(cross_walk_src) if cross_walk_src else dict()
        )

        if cross_walk_src and s3_bucket:
            # Remove temporary file
            os.remove(cross_walk_src)

        with transaction.atomic():
            merge_topics(guaranteed_links=guaranteed_links, verbose=True)
