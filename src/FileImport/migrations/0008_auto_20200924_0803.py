# Generated by Django 3.1.1 on 2020-09-24 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("FileImport", "0007_auto_20200924_0733"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fileimport",
            options={
                "verbose_name": "Data Import Log",
                "verbose_name_plural": "Data Import Logs",
            },
        ),
    ]
