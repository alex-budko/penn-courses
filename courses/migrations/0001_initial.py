# Generated by Django 2.2 on 2019-04-11 02:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.CharField(max_length=8)),
                ('code', models.CharField(max_length=8)),
                ('semester', models.CharField(max_length=5)),
                ('title', models.TextField()),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=16)),
                ('status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed'), ('X', 'Cancelled'), ('', 'Unlisted')], max_length=4)),
                ('capacity', models.IntegerField(default=0)),
                ('activity', models.CharField(blank=True, max_length=50, null=True)),
                ('meeting_times', models.TextField(blank=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('instructors', models.ManyToManyField(to='courses.Instructor')),
            ],
            options={
                'unique_together': {('code', 'course')},
            },
        ),
        migrations.CreateModel(
            name='StatusUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed'), ('X', 'Cancelled'), ('', 'Unlisted')], max_length=16)),
                ('new_status', models.CharField(choices=[('O', 'Open'), ('C', 'Closed'), ('X', 'Cancelled'), ('', 'Unlisted')], max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('alert_sent', models.BooleanField()),
                ('request_body', models.TextField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Section')),
            ],
        ),
    ]
