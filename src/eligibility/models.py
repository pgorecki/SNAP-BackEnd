import uuid
from django.db import models
from simple_history.models import HistoricalRecords
from agency.models import Agency
from client.models import Client
from core.models import ObjectRoot, User
from .enums import EligibilityStatus
from .managers import (
    EligibilityObjectManager,
    AgencyEligibilityConfigObjectManager,
    ClientEligibilityObjectManager,
    EligibilityQueueObjectManager,
)


class Eligibility(ObjectRoot):
    class Meta:
        verbose_name_plural = 'Eligibility'
        db_table = 'eligibility'
        ordering = ['-created_at']

    name = models.CharField(max_length=64)
    objects = EligibilityObjectManager()


class AgencyEligibilityConfig(ObjectRoot):
    class Meta:
        db_table = 'eligibility_agency_config'
        ordering = ['-created_at']

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    eligibility = models.ForeignKey(Eligibility, on_delete=models.CASCADE)

    objects = AgencyEligibilityConfigObjectManager()


class ClientEligibility(ObjectRoot):
    class Meta:
        db_table = 'eligibility_client'
        ordering = ['-created_at']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='eligibility')
    eligibility = models.ForeignKey(Eligibility, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32,
        choices=[(x.name, x.value) for x in EligibilityStatus]
    )
    effective_date = models.DateField(blank=True, null=True)
    history = HistoricalRecords()

    objects = ClientEligibilityObjectManager()

    @staticmethod
    def newest(cls, client):
        cls.objects.filter(client=client).first()


class EligibilityQueue(ObjectRoot):
    class Meta:
        db_table = 'eligibility_queue'
        ordering = ['-created_at']

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    requestor = models.ForeignKey(Agency, on_delete=models.CASCADE)
    status = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        choices=[(x.name, x.value) for x in EligibilityStatus]
    )
    resolved_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)

    objects = EligibilityQueueObjectManager()
