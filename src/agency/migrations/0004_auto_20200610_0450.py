# Generated by Django 3.0.7 on 2020-06-10 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("agency", "0003_auto_20200610_0424"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agency",
            name="programs",
        ),
        migrations.DeleteModel(
            name="Program",
        ),
    ]
