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
    end_reason = models.CharField(max_length=200,blank=True, null=True,help_text='MPR file column:Reason Participation Terminated')   #MPR
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

class EnrollmentActivity(ObjectRoot): 
    class Meta:
        db_table = 'program_enrollment_activity'
        ordering = ['id']

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='activities')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    qualifying_activity_name = models.CharField(max_length=64,blank=True, null=True,help_text='MPR file column:Qualifying Activity Enrolled')   #MPR 
    qualifying_activity_hours = models.IntegerField(blank=True, null=True,help_text='MPR file column:Qualifying Activity (51% or >) Hours')   #MPR
    billable_activity = models.CharField(max_length=6,blank=True, null=True,help_text='MPR file column:Is Qualifying Activity Billable (Y/N)')   #MPR
    non_qualifying_activity_hours = models.IntegerField(blank=True, null=True,help_text='MPR file column:Non-Qualifying Activity (49% or <) Hours')   #MPR
    required_number_of_articipatio_hours = models.IntegerField(blank=True, null=True,help_text='MPR file column:Required Number of Participation Hours')   #MPR
    actual_total_monthly_participation_hours = models.DecimalField(max_digits = 5, decimal_places = 2,null=True, help_text='MPR file column:Actual Total Monthly Participation Hours')   #MPR
    hours_met = models.CharField(max_length=6,blank=True, null=True,help_text='MPR file column:Was ABAWD Work Requirement Met (Y/N)')   #MPR
    performance_met = models.CharField(max_length=6,blank=True, null=True,help_text='MPR file column:Meeting Performance Standards (Y/N)')   #MPR
    # MPR 'If not Meeting Performance Standards, Please Explain' column will be stored in Note model
    month = models.CharField(max_length=60,blank=True, null=True,default='Service Month:  ',help_text='MPR month or period')   #MPR
    sheet = models.CharField(max_length=20,blank=True, null=True,default='October 1900',help_text='MPR sheet name')   #MPR
    provider = models.CharField(max_length=60,blank=True, null=True,default='(Provider Name)',help_text='MPR sheet name')   #MPR
    data_import_id = models.CharField(max_length=36,blank=True, null=True,help_text='MPR import job run instance')   #MPR
    actual_attendance_week = models.CharField(max_length=80,blank=True, null=True,help_text='MPR file column: Actual Attendance Week. Stored as dictionary string')

class AttendanceWeek(models.Model):                                                      #MPR
    class Meta:                                                                          #MPR
        db_table = 'program_enrollment_activity_attendanceweek'                          #MPR
        ordering = ['id']                                                                #MPR
    week = models.CharField(max_length=10,blank=True, null=True,help_text='MPR file column:Actual Attendance Week - week')   #MPR 
    hours = models.DecimalField(max_digits = 5, decimal_places = 2,null=True, help_text='MPR file column:Actual Attendance Week - hours')   #MPR
    activity = models.ForeignKey(EnrollmentActivity, on_delete=models.CASCADE, related_name='attendance_weeks')  #MPR
    
class EnrollmentService(ObjectRoot):
    class Meta:
        db_table = 'program_enrollment_service'
        ordering = ['id']
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='services')
    effective_date = models.DateField(blank=True, null=True)
    offered = models.CharField(max_length=6,blank=True, null=True,help_text='MPR file column:Support Service Offered (Y/N)')   #MPR
    type_and_amount = models.CharField(max_length=64,blank=True, null=True,help_text='MPR file column:Support Service Issued (Type & Amount)')   #MPR
    if_no_support_services_needed_explain_why = models.CharField(max_length=200,blank=True, null=True,help_text='MPR file column:If No Support Services Needed, Explain Why')   #MPR
    retention_services_type_amount = models.CharField(max_length=64,blank=True, null=True,help_text='MPR file column:Retention Services Provided (Type & Amount)')   #MPR
    # MPR Comments column will be stored in Note model
    data_import_id = models.CharField(max_length=36,blank=True, null=True,help_text='MPR import job run instance')   #MPR


        
        
        
    