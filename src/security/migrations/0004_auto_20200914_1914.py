# Generated by Django 3.1.1 on 2020-09-14 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("security", "0003_auto_20200707_1229"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="securitygroup",
            options={
                "ordering": ["name"],
                "verbose_name": "Security Group",
                "verbose_name_plural": "Security Groups",
            },
        ),
    ]
