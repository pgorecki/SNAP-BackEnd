# Generated by Django 3.0.8 on 2020-08-19 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eligibility', '0005_auto_20200814_1022'),
        ('iep', '0004_auto_20200819_0824'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientiep',
            name='eligibility_request',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='eligibility.EligibilityQueue'),
        ),
    ]
