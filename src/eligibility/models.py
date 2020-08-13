import uuid
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    # TODO: should be removed in the future?
    class Meta:
        verbose_name_plural = 'Eligibility'
        db_table = 'eligibility'
        ordering = ['-created_at']

    name = models.CharField(max_length=64)
    objects = EligibilityObjectManager()


class AgencyEligibilityConfig(ObjectRoot):
    # TODO: should be removed in the future?
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
    eligibility = models.ForeignKey(Eligibility, on_delete=models.CASCADE)  # TODO: should be removed in the future?
    status = models.CharField(
        max_length=32,
        choices=[(x.name, x.value) for x in EligibilityStatus]
    )
    effective_date = models.DateField(blank=True, null=True)
    history = HistoricalRecords()

    objects = ClientEligibilityObjectManager()

    @classmethod
    def is_eligible(cls, client):
        newest = cls.objects.filter(client=client).first()
        # TODO refactor enums to TextChoice
        is_eligible = newest is not None and newest.status == EligibilityStatus.ELIGIBLE.name
        return is_eligible


class EligibilityQueue(ObjectRoot):
    class Meta:
        db_table = 'eligibility_queue'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['client', 'requestor'], condition=Q(
                status=None), name='unique_eligilibity_request')
        ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    requestor = models.ForeignKey(Agency, on_delete=models.CASCADE)
    status = models.CharField(
        blank=True,
        null=True,
        max_length=32,
        # TODO refactor enums https://adamj.eu/tech/2020/01/27/moving-to-django-3-field-choices-enumeration-types/
        choices=[(x.name, x.value) for x in EligibilityStatus]
    )
    resolved_by = models.ForeignKey(User, on_delete=models.PROTECT, blank=True,
                                    null=True, related_name='resolved_eligibility')

    @property
    def is_resolved(self):
        return self.status is not None

    objects = EligibilityQueueObjectManager()


@receiver(post_save, sender=EligibilityQueue)
def update_client_eligibility(sender, instance, created, **kwargs):
    if instance._meta.model.objects.first() == instance and instance.is_resolved:
        instance.client.eligibility.create(
            status=instance.status,
            eligibility=Eligibility.objects.first()  # should be removed in the future?
        )
