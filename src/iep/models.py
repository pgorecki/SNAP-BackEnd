from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from core.models import ObjectRoot, User
from core.validation import model_validation, ModelValidationMixin
from eligibility.models import EligibilityQueue
from client.models import Client
from program.models import Enrollment
from .choices import IEPStatus


class ClientIEP(ObjectRoot):
    class Meta:
        db_table = 'iep_client'
        ordering = ['-created_at']

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='ieps')
    case_manager = models.ForeignKey(User, related_name='iep', on_delete=models.SET_NULL, null=True, blank=True)
    orientation_completed = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    eligibility_request = models.ForeignKey(
        EligibilityQueue, on_delete=models.SET_NULL, related_name='ieps', blank=True, null=True)
    projected_end_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=32,
        choices=IEPStatus.choices,
        default=IEPStatus.AWAITING_APPROVAL
    )
    outcome = models.CharField(max_length=64, default='', blank=True, help_text='Outcome when completed')


class ClientIEPEnrollment(ModelValidationMixin, models.Model):
    class Meta:
        db_table = 'iep_enrollment'
        ordering = ['id']

    iep = models.ForeignKey(ClientIEP, on_delete=models.CASCADE, related_name='iep_enrollments')
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, blank=True, null=True)

    # def clean(self):
    #     if self.iep and self.enrollment and self.iep.client.id != self.enrollment.client.id:
    #         raise ValidationError(
    #             f'IEP client id ({self.iep.client.id}) does not match enrollment client id ({self.enrollment.client.id})')

    #     self.iep.clean()


@receiver(model_validation, sender=Enrollment)
def validate_iep_Enrollment(sender, instance, *args, **kwargs):
    """
    When enrollment is save, check if it is an IEP enrollment and if the programs are the same
    """
    iep_enrollment = ClientIEPEnrollment.objects.filter(enrollment=instance).first()
    if iep_enrollment is None or iep_enrollment.iep is None:
        return

    iep = iep_enrollment.iep

    for other_iep_enrollment in iep.iep_enrollments.exclude(enrollment=instance):
        other_enrollment = other_iep_enrollment.enrollment
        if other_enrollment.program.agency != instance.program.agency:
            raise ValidationError(
                f'IEP enrollment programs {instance.program} and {other_enrollment.program} are not from same agency')


@receiver(model_validation, sender=ClientIEP)
def validate_iep_ClientIEP(sender, instance, *args, **kwargs):
    """
    When enrollment is save, check if it is an IEP enrollment and if the programs are the same
    """

    program = None

    for iep_enrollment in instance.iep_enrollments.all():
        enrollment = iep_enrollment.enrollment
        if program is None:
            program = enrollment.program
        elif enrollment.program.agency != program.agency:
            raise ValidationError(
                f'IEP enrollment programs {program} and {enrollment.program} are not from same agency')


@receiver(model_validation, sender=ClientIEPEnrollment)
def validate_client_consistency_ClientIEPEnrollment(sender, instance, *args, **kwargs):
    if instance.iep and instance.enrollment and instance.iep.client.id != instance.enrollment.client.id:
        raise ValidationError(
            f'IEP client id({instance.iep.client.id}) does not \
            match with enrollment client id({instance.enrollment.client.id})')


@receiver(model_validation, sender=Enrollment)
def validate_client_consistency_Enrollment(sender, instance, *args, **kwargs):
    print('validate_client_consistency_Enrollment')
    iep_enrollment = ClientIEPEnrollment.objects.filter(enrollment=instance).first()
    if iep_enrollment is None:
        return

    iep = iep_enrollment.iep
    if iep.client.id != instance.client.id:
        raise ValidationError(f'Enrollment client {instance.client.id} does not match to IEP client {iep.client.id}')


@receiver(post_save, sender=ClientIEP)
def update_client_is_new_field(sender, instance, created, **kwargs):
    ieps_in_progress = ClientIEP.objects.filter(status=IEPStatus.IN_PROGRESS).count()
    if ieps_in_progress:
        instance.client.is_new = False
    else:
        instance.client.is_new = True
    instance.client.save()
