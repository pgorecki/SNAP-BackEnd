# Generated by Django 3.1.1 on 2020-09-14 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("FileImport", "0003_auto_20200914_0634"),
    ]

    operations = [
        migrations.AddField(
            model_name="fileimport",
            name="xls_file",
            field=models.FileField(null=True, upload_to="xls_imports"),
        ),
    ]
