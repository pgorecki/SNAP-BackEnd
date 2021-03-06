# Generated by Django 3.0.8 on 2020-08-17 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0004_remove_client_is_removed"),
    ]

    operations = [
        migrations.CreateModel(
            name="ClientAddress",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(blank=True, default="", max_length=256)),
                ("city", models.CharField(blank=True, default="", max_length=64)),
                ("state", models.CharField(blank=True, default="", max_length=64)),
                ("zip", models.CharField(blank=True, default="", max_length=8)),
                ("county", models.CharField(blank=True, default="", max_length=64)),
            ],
            options={
                "db_table": "client_address",
            },
        ),
        migrations.AddField(
            model_name="client",
            name="snap_id",
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name="client",
            name="ssn",
            field=models.CharField(blank=True, default="", max_length=64),
        ),
        migrations.AddField(
            model_name="client",
            name="address",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="client.ClientAddress",
            ),
        ),
    ]
