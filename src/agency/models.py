from django.db import models
from core.models import ObjectRoot
from client.models import Client


class Agency(ObjectRoot):
    class Meta:
        db_table = 'agency'
        verbose_name_plural = 'Agencies'
    name = models.CharField(max_length=64)
    programs = models.ManyToManyField('program.Program', related_name='agencies',
                                      through='program.AgencyProgramConfig')
    eligibility = models.ManyToManyField(
        'eligibility.Eligibility', related_name='eligibility', through='eligibility.AgencyEligibilityConfig')

    def __str__(self):
        return self.name


class AgencyClient(models.Model):
    class Meta:
        db_table = 'agency_client'
    client = models.ForeignKey(
        Client, related_name='agency_clients', on_delete=models.PROTECT)
    agency = models.ForeignKey(
        Agency, related_name='agency_clients', on_delete=models.PROTECT)
