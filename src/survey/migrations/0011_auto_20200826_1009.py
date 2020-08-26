# Generated by Django 3.1 on 2020-08-26 10:09

from django.db import migrations


def move_respondent_to_client(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Response = apps.get_model('survey', 'Response')
    for r in Response.objects.all():
        print(dir(r))
        r.client_id = r.respondent_id
        r.save()


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0010_auto_20200826_1008'),
    ]

    operations = [
        migrations.RunPython(move_respondent_to_client),
    ]
