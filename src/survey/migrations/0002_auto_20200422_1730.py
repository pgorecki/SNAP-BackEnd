# Generated by Django 3.0.5 on 2020-04-22 17:30

import core.json_yaml_field
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="survey",
            name="is_public",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="survey",
            name="definition",
            field=core.json_yaml_field.JsonYamlField(),
        ),
    ]
