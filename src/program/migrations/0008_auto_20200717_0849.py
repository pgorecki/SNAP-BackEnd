# Generated by Django 3.0.8 on 2020-07-17 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('program', '0007_auto_20200709_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencyprogramconfig',
            name='is_removed',
        ),
        migrations.RemoveField(
            model_name='enrollment',
            name='is_removed',
        ),
        migrations.RemoveField(
            model_name='historicalenrollment',
            name='is_removed',
        ),
        migrations.RemoveField(
            model_name='historicalprogrameligibility',
            name='is_removed',
        ),
        migrations.RemoveField(
            model_name='program',
            name='is_removed',
        ),
        migrations.RemoveField(
            model_name='programeligibility',
            name='is_removed',
        ),
    ]
