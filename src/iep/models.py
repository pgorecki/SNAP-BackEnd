from django.db import models
from core.models import ObjectRoot, User
from client.models import Client
from program.models import Enrollment
from .choices import IEPStatus


class ClientIEP(ObjectRoot):
    class Meta:
        db_table = 'iep_client'
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='iep')
    case_manager = models.ForeignKey(User, related_name='iep', on_delete=models.SET_NULL, null=True)
    orientation_completed = models.BooleanField(default=False)
    status = models.CharField(
        max_length=32,
        choices=IEPStatus.choices,
        default=IEPStatus.AWAITING_APPROVAL
    )
    outcome = models.CharField(max_length=64, default='', blank=True, help_text='Outcome when completed')


class ClientIEPEnrollment(models.Model):
    class Meta:
        db_table = 'iep_enrollment'

    iep = models.ForeignKey(ClientIEP, on_delete=models.CASCADE)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, blank=True, null=True)
