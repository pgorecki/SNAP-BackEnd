# Generated by Django 3.0.8 on 2020-08-18 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_auto_20200817_1226'),
        ('program', '0010_auto_20200817_1230'),
        ('iep', '0002_auto_20200817_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientiep',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ieps', to='client.Client'),
        ),
        migrations.AlterField(
            model_name='clientiepenrollment',
            name='enrollment',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='program.Enrollment'),
        ),
        migrations.AlterField(
            model_name='clientiepenrollment',
            name='iep',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iep_enrollments', to='iep.ClientIEP'),
        ),
    ]
