# Generated by Django 3.1.1 on 2020-09-14 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iep', '0012_auto_20200914_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientiep',
            name='job_placement',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='iep.jobplacement'),
        ),
    ]