# Generated by Django 3.0.7 on 2020-07-07 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("program", "0005_auto_20200707_0933"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="program",
            options={"ordering": ["name"]},
        ),
    ]
