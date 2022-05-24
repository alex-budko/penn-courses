from decimal import Decimal

from django.db.models import Count, Q
from django.db.models.expressions import F, Subquery
from rest_framework import filters

from courses.models import Attribute, Meeting, PreNGSSRequirement, Section
from courses.util import get_current_semester
from plan.models import Schedule


def section_ids_by_meeting_query(meeting_query):
    """
    Returns a queryset of the ids of sections for which all meetings pass the
    given meeting query.
    """
    return (
        Meeting.objects.filter(meeting_query)
        .values("section")
        .annotate(num_matching_meetings=Count("id"))
        .order_by()
        .filter(section__num_meetings=F("num_matching_meetings"))
        .values("section_id")
        .distinct()
    )


def course_ids_by_section_query(section_query):
    """
    Returns a queryset of the ids of courses for which at least one section
    of each activity type passes the given section query.
    """
    return (
        Section.objects.filter(section_query)
        .values("course")
        .annotate(num_matching_activities=Count("activity", distinct=True))
        .order_by()
        .filter(course__num_activities=F("num_matching_activities"))
        .values("course_id")
        .distinct()
    )


def meeting_filter(queryset, meeting_query):
    """
    Filters the given queryset of courses by the following condition:
    include a course only if the specified meeting filter
    (meeting_query, represented as a Q() query object)
    does not limit the set of section activities we can participate in for the course.
    For instance, if meeting_query=Q(day__in={"T","W","R"}),
    then we would include a course with lecture and recitation sections only if
    we could enroll in some lecture section and some recitation section and
    only have to attend meetings on Tuesdays, Wednesdays, and/or Thursdays.
    However, if the course had a lab section that only met on Fridays,
    we would no longer include the course (since we cannot attend the meetings of the
    lab section, and thus the set of course activities available to us is incomplete).
    """
    return queryset.filter(
        id__in=course_ids_by_section_query(
            Q(num_meetings=0) | Q(id__in=section_ids_by_meeting_query(meeting_query))
        )
    )


def is_open_filter(queryset, *args):
    """
    Filters the given queryset of courses by the following condition:
    include a course only if filtering its sections by `status="O"` does
    not does not limit the set of section activities we can participate in for the course.
    In other words, include only courses for which all activities have open sections.
    Note that for compatibility, this function can take additional positional
    arguments, but these are ignored.
    """
    return queryset.filter(id__in=course_ids_by_section_query(Q(status="O")))


def day_filter(days):
    """
    Constructs a Q() query object for filtering meetings by day,
    based on the given days filter string.
    """
    days = set(days)
    if not days.issubset({"M", "T", "W", "R", "F", "S", "U"}):
        return Q()
    return Q(day__isnull=True) | Q(day__in=set(days))


def time_filter(time_range):
    """
    Constructs a Q() query object for filtering meetings by start/end time,
    based on the given time_range filter string.
    """
    if not time_range:
        return Q()
    times = time_range.split("-")
    if len(times) != 2:
        return Q()
    times = [t.strip() for t in times]
    for time in times:
        if time and not time.replace(".", "", 1).isdigit():
            return Q()
    start_time, end_time = times
    query = Q()
    if start_time:
        query &= Q(start__isnull=True) | Q(start__gte=Decimal(start_time))
    if end_time:
        query &= Q(end__isnull=True) | Q(end__lte=Decimal(end_time))
    return query


def gen_schedule_filter(request):
    """
    Generates a schedule filter function that checks for proper
    authentication in the given request.
    """

    def schedule_filter(schedule_id):
        """
        Constructs a Q() query object for filtering meetings by
        whether they fit into the specified schedule.
        """
        if not schedule_id:
            return Q()
        if not schedule_id.isdigit():
            return Q()
        if not request.user.is_authenticated:
            return Q()
        meetings = Meeting.objects.filter(
            section_id__in=Subquery(
                Schedule.objects.filter(id=int(schedule_id), person_id=request.user.id).values(
                    "sections__id"
                )
            )
        )
        query = Q()
        for meeting in meetings:
            query &= meeting.no_conflict_query
        return query

    return schedule_filter


def pre_ngss_requirement_filter(queryset, req_ids):
    if not req_ids:
        return queryset
    query = Q()
    for req_id in req_ids.split(","):
        code, school = req_id.split("@")
        try:
            requirement = PreNGSSRequirement.objects.get(
                code=code, school=school, semester=get_current_semester()
            )
        except PreNGSSRequirement.DoesNotExist:
            continue
        query &= Q(id__in=requirement.satisfying_courses.all())

    return queryset.filter(query)


def attribute_filter(queryset, attr_ids):
    """
    :param queryset: initial Course object queryset
    :param attr_ids: the attribute codes (ex: WUOM) comma seperated
    :return: filtered queryset
    """
    if not attr_ids:
        return queryset
    query = Q()
    for attr_id in attr_ids.split(","):
        try:
            attribute = Attribute.objects.get(code=attr_id)
        except Attribute.DoesNotExist:
            continue
        query |= Q(id__in=attribute.courses.all())
    return queryset.filter(query)


def bound_filter(field):
    def filter_bounds(queryset, bounds):
        if not bounds:
            return queryset
        bound_arr = bounds.split("-")
        if len(bound_arr) != 2:
            return queryset
        bound_arr = [b.strip() for b in bound_arr]
        for bound in bound_arr:
            if bound and not bound.replace(".", "", 1).isdigit():
                return queryset
        lower_bound, upper_bound = bound_arr
        lower_bound = Decimal(lower_bound)
        upper_bound = Decimal(upper_bound)

        return queryset.filter(
            Q(**{f"{field}__isnull": True})
            | Q(
                **{
                    f"{field}__gte": lower_bound,
                    f"{field}__lte": upper_bound,
                }
            )
        )

    return filter_bounds


def choice_filter(field):
    def filter_choices(queryset, choices):
        if not choices:
            return queryset
        query = Q()
        for choice in choices.split(","):
            query = query | Q(**{field: choice})

        return queryset.filter(query)

    return filter_choices


class CourseSearchFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filters = {
            "attributes": attribute_filter,
            "pre_ngss_requirements": pre_ngss_requirement_filter,
            "cu": choice_filter("sections__credits"),
            "activity": choice_filter("sections__activity"),
            "course_quality": bound_filter("course_quality"),
            "instructor_quality": bound_filter("instructor_quality"),
            "difficulty": bound_filter("difficulty"),
            "is_open": is_open_filter,
        }
        for field, filter_func in filters.items():
            param = request.query_params.get(field)
            if param is not None:
                queryset = filter_func(queryset, param)

        # Combine meeting filter queries for efficiency
        meeting_filters = {
            "days": day_filter,
            "time": time_filter,
            "schedule-fit": gen_schedule_filter(request),
        }
        meeting_query = Q()
        for field, filter_func in meeting_filters.items():
            param = request.query_params.get(field)
            if param is not None:
                meeting_query &= filter_func(param)
        if len(meeting_query) > 0:
            queryset = meeting_filter(queryset, meeting_query)

        return queryset.distinct()

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": "type",
                "required": False,
                "in": "query",
                "description": "Can specify what kind of query to run. Course queries are faster, "
                "keyword queries look against professor name and course title.",
                "schema": {
                    "type": "string",
                    "default": "auto",
                    "enum": ["auto", "course", "keyword"],
                },
            },
            {
                "name": "pre_ngss_requirements",
                "required": False,
                "in": "query",
                "description": "Deprecated since 2022C. Filter courses by comma-separated pre"
                               "ngss requirements, ANDed together. Use `/requirements` endpoint"
                               "to get requirement IDs.",
                "schema": {"type": "string"},
                "example": "SS@SEAS,H@SEAS",
            },
            {
                "name": "attributes",
                "required": False,
                "in": "query",
                "description": "Filter courses by comma-separated attributes, ORed together."
                "Use `/attributes` endpoint to get attribute codes.",
                "schema": {"type": "string"},
                "example": "WUOM,WUGA",
            },
            {
                "name": "cu",
                "required": False,
                "in": "query",
                "description": "Filter course units to be within the given range.",
                "schema": {"type": "string"},
                "example": "0-0.5",
            },
            {
                "name": "difficulty",
                "required": False,
                "in": "query",
                "description": (
                    "Filter course difficulty (average across all reviews) to be within "
                    "the given range."
                ),
                "schema": {"type": "string"},
                "example": "1-2.5",
            },
            {
                "name": "course_quality",
                "required": False,
                "in": "query",
                "description": (
                    "Filter course quality (average across all reviews) to be within "
                    "the given range."
                ),
                "schema": {"type": "string"},
                "example": "2.5-4",
            },
            {
                "name": "instructor_quality",
                "required": False,
                "in": "query",
                "description": (
                    "Filter instructor quality (average across all reviews) to be "
                    "within the given range."
                ),
                "schema": {"type": "string"},
                "example": "2.5-4",
            },
            {
                "name": "days",
                "required": False,
                "in": "query",
                "description": (
                    "Filter meetings to be within the specified set of days. "
                    "The set of days should be specified as a string containing some "
                    "combination of the characters [M, T, W, R, F, S, U]. "
                    "This filters courses by the following condition: "
                    "include a course only if the specified day filter "
                    "does not limit the set of section activities we can participate in "
                    "for the course. "
                    "Passing an empty string will return only asynchronous classes "
                    "or classes with meeting days TBD."
                ),
                "schema": {"type": "string"},
                "example": "TWR",
            },
            {
                "name": "time",
                "required": False,
                "in": "query",
                "description": (
                    "Filter meeting times to be within the specified range. "
                    "The start and end time of the filter should be dash-separated. "
                    "Times should be specified as decimal numbers of the form `h+mm/100` "
                    "where h is the hour `[0..23]` and mm is the minute `[0,60)`, in ET. "
                    "You can omit either the start or end time to leave that side unbounded, "
                    "e.g. '11.30-'. "
                    "This filters courses by the following condition: "
                    "include a course only if the specified time filter "
                    "does not limit the set of section activities we can participate in "
                    "for the course."
                ),
                "schema": {"type": "string"},
                "example": "11.30-18",
            },
            {
                "name": "schedule-fit",
                "required": False,
                "in": "query",
                "description": (
                    "Filter meeting times to fit into the schedule with the specified integer id. "
                    "You must be authenticated with the account owning the specified schedule, "
                    "or this filter will be ignored. "
                    "This filters courses by the following condition: "
                    "include a course only if the specified schedule-fit filter "
                    "does not limit the set of section activities we can participate in "
                    "for the course."
                ),
                "schema": {"type": "integer"},
                "example": "242",
            },
            {
                "name": "is_open",
                "required": False,
                "in": "query",
                "description": (
                    "Filter courses to only those that are open. "
                    "A boolean of true should be included if you want to apply the filter. "
                    "By default (ie when the `is_open` is not supplied, the filter is not applied. "
                    "This filters courses by the following condition: "
                    "include a course only if the specification that a section is open "
                    "does not limit the set of section activities we can participate in "
                    "for the course."
                    "In other words, filter to courses for which all activities have open sections."
                ),
                "schema": {"type": "boolean"},
                "example": "true",
            },
        ]
