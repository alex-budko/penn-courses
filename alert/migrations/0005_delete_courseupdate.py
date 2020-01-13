# Generated by Django 2.2.5 on 2019-09-28 20:36

from django.db import migrations


def forwards(apps, schema_editor):
    CourseUpdate = apps.get_model('alert', 'CourseUpdate')
    StatusUpdate = apps.get_model('courses', 'StatusUpdate')
    for old_up in CourseUpdate.objects.all():
        new_up = StatusUpdate.objects.create(section=old_up.section,
                                             old_status=old_up.old_status,
                                             new_status=old_up.new_status,
                                             created_at=old_up.created_at,
                                             alert_sent=old_up.alert_sent,
                                             request_body=old_up.request_body)
        new_up.save()

def backwards(apps, schema_editor):
    CourseUpdate = apps.get_model('alert', 'CourseUpdate')
    StatusUpdate = apps.get_model('courses', 'StatusUpdate')
    for old_up in StatusUpdate.objects.all():
        new_up = CourseUpdate.objects.create(section=old_up.section,
                                             old_status = old_up.old_status,
                                             new_status = old_up.old_status,
                                             created_at = old_up.created_at,
                                             alert_sent = old_up.alert_sent,
                                             request_body = old_up.request_body)
        new_up.save()


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0004_auto_20190926_0549'),
    ]

    operations = [
        migrations.RunPython(
            forwards,
            backwards
        ),
        migrations.DeleteModel(
            name='CourseUpdate',
        ),
    ]
