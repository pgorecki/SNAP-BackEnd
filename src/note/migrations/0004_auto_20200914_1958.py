# Generated by Django 3.1.1 on 2020-09-14 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("note", "0003_remove_note_is_removed"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="title",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="note",
            name="text",
            field=models.TextField(blank=True, default=""),
        ),
    ]
