# Generated by Django 3.1.1 on 2020-09-09 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("iep", "0009_auto_20200901_1926"),
    ]

    operations = [
        migrations.AddField(
            model_name="clientiep",
            name="abawd",
            field=models.CharField(
                blank=True,
                help_text="MPR file column: ABAWD (Y/N)",
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="clientiep",
            name="case_number",
            field=models.CharField(
                blank=True,
                help_text="MPR file column: Case Number",
                max_length=36,
                null=True,
            ),
        ),
    ]
