from django.db import models
from core.models import ObjectRoot
from core.managers import AgencyObjectManager


class ClientAddress(models.Model):
    class Meta:
        db_table = 'client_address'
        verbose_name='Client Address'
        verbose_name_plural = 'Client Addresses'

    street = models.CharField(max_length=256, blank=True, default='')
    city = models.CharField(max_length=64, blank=True, default='')
    state = models.CharField(max_length=64, blank=True, default='')
    zip = models.CharField(max_length=8, blank=True, default='')
    county = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        return f'{self.street} {self.city} {self.state} {self.zip}'


class Client(ObjectRoot):
    class Meta:
        db_table = 'client'
        ordering = ['-created_at']
        permissions = (
            ('view_client_agency', 'Can view client - agency'),
            ('change_client_agency', 'Can change client - agency'),
            ('delete_client_agency', 'Can delete client - agency'),
            ('view_client_all', 'Can view client - globally'),
            ('change_client_all', 'Can change client - globally'),
            ('delete_client_all', 'Can delete client - globally'),
        )

    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, default='', blank=True)
    last_name = models.CharField(max_length=64)
    dob = models.DateField(null=True)                                     #MPR (MPR file does not contain dob column, therefore null=True)
    ssn = models.CharField(max_length=64, blank=True, default='')
    is_new = models.BooleanField(default=True)

    snap_id = models.CharField(max_length=256, blank=True, null=True)
    address = models.OneToOneField(ClientAddress, on_delete=models.CASCADE, null=True)

    objects = AgencyObjectManager()

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join([p for p in parts if p])

    def __str__(self):
        return self.full_name
