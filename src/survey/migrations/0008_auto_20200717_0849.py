# Generated by Django 3.0.8 on 2020-07-17 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0007_auto_20200717_0645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='is_removed',
        ),
        migrations.RemoveField(
            model_name='response',
            name='is_removed',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='is_removed',
        ),
    ]