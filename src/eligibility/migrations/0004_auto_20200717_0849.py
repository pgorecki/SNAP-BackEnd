# Generated by Django 3.0.8 on 2020-07-17 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("eligibility", "0003_auto_20200709_1020"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agencyeligibilityconfig",
            name="is_removed",
        ),
        migrations.RemoveField(
            model_name="clienteligibility",
            name="is_removed",
        ),
        migrations.RemoveField(
            model_name="eligibility",
            name="is_removed",
        ),
        migrations.RemoveField(
            model_name="historicalclienteligibility",
            name="is_removed",
        ),
    ]
