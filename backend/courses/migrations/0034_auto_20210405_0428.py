# Generated by Django 3.2b1 on 2021-04-05 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0033_statusupdate_in_add_drop_period"),
    ]

    operations = [
        migrations.AddField(
            model_name="statusupdate",
            name="percent_through_add_drop_period",
            field=models.DecimalField(
                blank=True,
                decimal_places=4,
                help_text="The percentage through the add/drop period at which this status update occurred.This percentage is constrained within the range [0,1].",
                max_digits=6,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="latitude",
            field=models.FloatField(
                blank=True,
                help_text="\nThe latitude of the building, in the signed decimal degrees format (global range of\n[-90.0, 90.0]), e.g. `39.961380` for the Towne Building.\n",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="building",
            name="longitude",
            field=models.FloatField(
                blank=True,
                help_text="\nThe longitude of the building, in the signed decimal degrees format (global range of\n[-180.0, 180.0]), e.g. `-75.176773` for the Towne Building.\n",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="code",
            field=models.CharField(
                db_index=True, help_text="The course code, e.g. `120` for CIS-120.", max_length=8
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="full_code",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="The dash-joined department and code of the course, e.g. `CIS-120` for CIS-120.",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="semester",
            field=models.CharField(
                db_index=True,
                help_text="\nThe semester of the course (of the form YYYYx where x is A [for spring],\nB [summer], or C [fall]), e.g. `2019C` for fall 2019.\n",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="code",
            field=models.CharField(
                db_index=True,
                help_text="The department code, e.g. `CIS` for the CIS department.",
                max_length=8,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="code",
            field=models.CharField(
                db_index=True,
                help_text="\nThe code identifying this requirement, e.g. `MFR` for 'Formal Reasoning Course',\nan SAS requirement satisfied by CIS-120.\n",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="school",
            field=models.CharField(
                choices=[("SEAS", "Engineering"), ("WH", "Wharton"), ("SAS", "College")],
                db_index=True,
                help_text='\nWhat school this requirement belongs to, e.g. `SAS` for the SAS \'Formal Reasoning Course\'\nrequirement satisfied by CIS-120. Options and meanings:\n<table width=100%><tr><td>"SEAS"</td><td>"Engineering"</td></tr><tr><td>"WH"</td><td>"Wharton"</td></tr><tr><td>"SAS"</td><td>"College"</td></tr></table>',
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="requirement",
            name="semester",
            field=models.CharField(
                db_index=True,
                help_text="\nThe semester of the requirement (of the form YYYYx where x is A [for spring], B [summer],\nor C [fall]), e.g. `2019C` for fall 2019. We organize requirements by semester so that we\ndon't get huge related sets which don't give particularly good info.\n",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="room",
            name="number",
            field=models.CharField(
                help_text="The room number, e.g. `101` for Wu and Chen Auditorium in Levine.",
                max_length=5,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="activity",
            field=models.CharField(
                choices=[
                    ("CLN", "Clinic"),
                    ("DIS", "Dissertation"),
                    ("IND", "Independent Study"),
                    ("LAB", "Lab"),
                    ("LEC", "Lecture"),
                    ("MST", "Masters Thesis"),
                    ("REC", "Recitation"),
                    ("SEM", "Seminar"),
                    ("SRT", "Senior Thesis"),
                    ("STU", "Studio"),
                    ("***", "Undefined"),
                ],
                db_index=True,
                help_text='The section activity, e.g. `LEC` for CIS-120-001 (2020A). Options and meanings: <table width=100%><tr><td>"CLN"</td><td>"Clinic"</td></tr><tr><td>"DIS"</td><td>"Dissertation"</td></tr><tr><td>"IND"</td><td>"Independent Study"</td></tr><tr><td>"LAB"</td><td>"Lab"</td></tr><tr><td>"LEC"</td><td>"Lecture"</td></tr><tr><td>"MST"</td><td>"Masters Thesis"</td></tr><tr><td>"REC"</td><td>"Recitation"</td></tr><tr><td>"SEM"</td><td>"Seminar"</td></tr><tr><td>"SRT"</td><td>"Senior Thesis"</td></tr><tr><td>"STU"</td><td>"Studio"</td></tr><tr><td>"***"</td><td>"Undefined"</td></tr></table>',
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="capacity",
            field=models.IntegerField(
                default=0,
                help_text="The number of allowed registrations for this section, e.g. `220` for CIS-120-001 (2020A).",
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="code",
            field=models.CharField(
                db_index=True,
                help_text="The section code, e.g. `001` for the section CIS-120-001.",
                max_length=16,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="full_code",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="\nThe full code of the section, in the form '{dept code}-{course code}-{section code}',\ne.g. `CIS-120-001` for the 001 section of CIS-120.\n",
                max_length=32,
            ),
        ),
        migrations.AlterField(
            model_name="section",
            name="meeting_times",
            field=models.TextField(
                blank=True,
                help_text='\nA JSON-stringified list of meeting times of the form\n`{days code} {start time} - {end time}`, e.g.\n`["MWF 09:00 AM - 10:00 AM","F 11:00 AM - 12:00 PM","T 05:00 PM - 06:00 PM"]` for\nPHYS-151-001 (2020A). Each letter of the days code is of the form M, T, W, R, F for each\nday of the work week, respectively (and multiple days are combined with concatenation).\nTo access the Meeting objects for this section, the related field `meetings` can be used.\n',
            ),
        ),
    ]
