# Generated by Django 3.0.8 on 2020-08-17 12:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('program', '0010_auto_20200817_1230'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0006_auto_20200817_1226'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientIEP',
            fields=[
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created_at')),
                ('modified_at', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified_at')),
                ('orientation_completed', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('awaiting_approval', 'Awaiting approval'), ('in_progress', 'In progress'), ('ended', 'Ended')], default='awaiting_approval', max_length=32)),
                ('outcome', models.CharField(max_length=64)),
                ('case_manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='iep', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iep', to='client.Client')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'iep_client',
            },
        ),
        migrations.CreateModel(
            name='ClientIEPProgramStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('planned', 'Planned'), ('enrolled', 'Enrolled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='planned', max_length=16)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='iep_programs_status', to='iep.ClientIEP')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='program.Program')),
            ],
            options={
                'db_table': 'iep_program',
            },
        ),
    ]