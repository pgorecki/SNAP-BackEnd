import uuid
from django.db import models
from simple_history.models import HistoricalRecords
from core.models import ObjectRoot
from agency.models import Agency
from client.models import Client
from survey.models import Survey, Response
from .enums import EnrollmentStatus, ProgramEligibilityStatus
from .managers import (
    ProgramObjectManager,
    ProgramEligibilityObjectManager, EnrollmentObjectManager,
)


class Program(ObjectRoot):
    class Meta:
        db_table = 'program'
        ordering = ['name']

    agency = models.ForeignKey(Agency, null=True, related_name='programs', on_delete=models.SET_NULL)
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')

    enrollment_entry_survey = models.ForeignKey(
        Survey, related_name='programs_where_is_entry_survey', null=True, blank=True, on_delete=models.SET_NULL)
    enrollment_update_survey = models.ForeignKey(
        Survey, related_name='programs_where_is_update_survey', null=True, blank=True, on_delete=models.SET_NULL)
    enrollment_exit_survey = models.ForeignKey(
        Survey, related_name='programs_where_is_exit_survey', null=True, blank=True, on_delete=models.SET_NULL)

    objects = ProgramObjectManager()

    def __str__(self):
        return self.name


class Enrollment(ObjectRoot):
    class Meta:
        ordering = ['-created_at']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='enrollments')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='enrollments')
    start_date = models.DateField(blank=True, null=True)
    projected_end_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=32,
        choices=[(x.name, x.value) for x in EnrollmentStatus]
    )
    response = models.ForeignKey(Response, on_delete=models.SET_NULL,
                                 related_name='enrollment', blank=True, null=True)
    history = HistoricalRecords()

    objects = EnrollmentObjectManager()

    def __str__(self):
        return f"{self.id}"


# TODO remove, not used
class ProgramEligibility(ObjectRoot):
    class Meta:
        verbose_name_plural = 'Program eligibility'
        ordering = ['-created_at']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='program_eligibility')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_eligibility')
    status = models.CharField(
        max_length=32,
        choices=[(x.name, x.value) for x in ProgramEligibilityStatus]
    )
    history = HistoricalRecords()

    objects = ProgramEligibilityObjectManager()


class EnrollmentActivity(models.Model):
    class Meta:
        db_table = 'program_enrollment_activity'
        ordering = ['id']

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='activities')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)


class EnrollmentService(models.Model):
    class Meta:
        db_table = 'program_enrollment_service'
        ordering = ['id']
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='services')
    effective_date = models.DateField(blank=True, null=True)
