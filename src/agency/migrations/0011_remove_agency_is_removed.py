# Generated by Django 3.0.8 on 2020-07-17 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0010_auto_20200707_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agency',
            name='is_removed',
        ),
    ]