# Generated by Django 3.1.1 on 2020-09-24 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FileImport", "0006_auto_20200921_0833"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="fileimport",
            options={},
        ),
        migrations.AlterField(
            model_name="fileimport",
            name="file_path",
            field=models.CharField(
                blank=True,
                help_text="Path of file to be imported including the file name",
                max_length=200,
                null=True,
            ),
        ),
    ]
