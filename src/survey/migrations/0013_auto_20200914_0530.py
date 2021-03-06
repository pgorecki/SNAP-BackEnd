# Generated by Django 3.1.1 on 2020-09-14 05:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("survey", "0012_auto_20200826_1013"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="response",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="survey.response",
            ),
        ),
    ]
