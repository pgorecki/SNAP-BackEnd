# Generated by Django 3.0.7 on 2020-07-09 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matching', '0003_auto_20200707_0933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='matchingconfig',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='matchingconfig',
            name='name',
            field=models.CharField(default='config', max_length=256),
            preserve_default=False,
        ),
    ]