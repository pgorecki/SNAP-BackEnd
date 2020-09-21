# Generated by Django 3.1.1 on 2020-09-09 05:58

import core.validation
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("program", "0010_auto_20200817_1230"),
    ]

    operations = [
        migrations.AddField(
            model_name="enrollment",
            name="end_reason",
            field=models.CharField(
                blank=True,
                help_text="MPR file column:Reason Participation Terminated",
                max_length=200,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalenrollment",
            name="end_reason",
            field=models.CharField(
                blank=True,
                help_text="MPR file column:Reason Participation Terminated",
                max_length=200,
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="EnrollmentService",
            fields=[
                (
                    "id",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created_at",
                    ),
                ),
                (
                    "modified_at",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified_at",
                    ),
                ),
                ("effective_date", models.DateField(blank=True, null=True)),
                (
                    "offered",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Support Service Offered (Y/N)",
                        max_length=6,
                        null=True,
                    ),
                ),
                (
                    "type_and_amount",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Support Service Issued (Type & Amount)",
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "if_no_support_services_needed_explain_why",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:If No Support Services Needed, Explain Why",
                        max_length=200,
                        null=True,
                    ),
                ),
                (
                    "retention_services_type_amount",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Retention Services Provided (Type & Amount)",
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "data_import_id",
                    models.CharField(
                        blank=True,
                        help_text="MPR import job run instance",
                        max_length=36,
                        null=True,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "enrollment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="services",
                        to="program.enrollment",
                    ),
                ),
            ],
            options={
                "db_table": "program_enrollment_service",
                "ordering": ["id"],
            },
            bases=(core.validation.ModelValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name="EnrollmentActivity",
            fields=[
                (
                    "id",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created_at",
                    ),
                ),
                (
                    "modified_at",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified_at",
                    ),
                ),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "qualifying_activity_name",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Qualifying Activity Enrolled",
                        max_length=64,
                        null=True,
                    ),
                ),
                (
                    "qualifying_activity_hours",
                    models.IntegerField(
                        blank=True,
                        help_text="MPR file column:Qualifying Activity (51% or >) Hours",
                        null=True,
                    ),
                ),
                (
                    "billable_activity",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Is Qualifying Activity Billable (Y/N)",
                        max_length=6,
                        null=True,
                    ),
                ),
                (
                    "non_qualifying_activity_hours",
                    models.IntegerField(
                        blank=True,
                        help_text="MPR file column:Non-Qualifying Activity (49% or <) Hours",
                        null=True,
                    ),
                ),
                (
                    "required_number_of_articipatio_hours",
                    models.IntegerField(
                        blank=True,
                        help_text="MPR file column:Required Number of Participation Hours",
                        null=True,
                    ),
                ),
                (
                    "actual_total_monthly_participation_hours",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="MPR file column:Actual Total Monthly Participation Hours",
                        max_digits=5,
                        null=True,
                    ),
                ),
                (
                    "hours_met",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Was ABAWD Work Requirement Met (Y/N)",
                        max_length=6,
                        null=True,
                    ),
                ),
                (
                    "performance_met",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Meeting Performance Standards (Y/N)",
                        max_length=6,
                        null=True,
                    ),
                ),
                (
                    "month",
                    models.CharField(
                        blank=True,
                        default="Service Month:  ",
                        help_text="MPR month or period",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "sheet",
                    models.CharField(
                        blank=True,
                        default="October 1900",
                        help_text="MPR sheet name",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "provider",
                    models.CharField(
                        blank=True,
                        default="(Provider Name)",
                        help_text="MPR sheet name",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "data_import_id",
                    models.CharField(
                        blank=True,
                        help_text="MPR import job run instance",
                        max_length=36,
                        null=True,
                    ),
                ),
                (
                    "actual_attendance_week",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column: Actual Attendance Week. Stored as dictionary string",
                        max_length=80,
                        null=True,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "enrollment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="activities",
                        to="program.enrollment",
                    ),
                ),
            ],
            options={
                "db_table": "program_enrollment_activity",
                "ordering": ["id"],
            },
            bases=(core.validation.ModelValidationMixin, models.Model),
        ),
        migrations.CreateModel(
            name="AttendanceWeek",
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
                (
                    "week",
                    models.CharField(
                        blank=True,
                        help_text="MPR file column:Actual Attendance Week - week",
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "hours",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="MPR file column:Actual Attendance Week - hours",
                        max_digits=5,
                        null=True,
                    ),
                ),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendance_weeks",
                        to="program.enrollmentactivity",
                    ),
                ),
            ],
            options={
                "db_table": "program_enrollment_activity_attendanceweek",
                "ordering": ["id"],
            },
        ),
    ]
