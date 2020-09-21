# Generated by Django 3.1 on 2020-09-03 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0008_client_is_new"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="client",
            options={
                "ordering": ["-created_at"],
                "permissions": (
                    ("view_client_agency", "Can view client - agency"),
                    ("change_client_agency", "Can change client - agency"),
                    ("delete_client_agency", "Can delete client - agency"),
                    ("view_client_all", "Can view client - globally"),
                    ("change_client_all", "Can change client - globally"),
                    ("delete_client_all", "Can delete client - globally"),
                ),
            },
        ),
    ]
