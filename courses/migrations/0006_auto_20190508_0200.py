# Generated by Django 2.2 on 2019-05-08 02:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20190428_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='primary_listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_set', to='courses.Course'),
        ),
    ]
