from django.db import models
from core.models import ObjectRoot
from core.managers import AgencyObjectManager


class Client(ObjectRoot):
    class Meta:
        db_table = 'client'
        ordering = ['-created_at']
        # permissions = [
        #     ("view", "Can change the status of tasks"),
        # ]
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, default='', blank=True)
    last_name = models.CharField(max_length=64)
    dob = models.DateField()
    ssn = models.CharField(max_length=64, blank=True, default='')

    snap_id = models.CharField(max_length=256, blank=True, null=True)

    objects = AgencyObjectManager()

    @property
    def full_name(self):
        parts = [self.first_name, self.middle_name, self.last_name]
        return ' '.join([p for p in parts if p])

    def __str__(self):
        return self.full_name


class ClientAddress(models.Model):
    class Meta:
        db_table = 'client_address'

    client = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)

    address = models.CharField(max_length=256, blank=True, default='')
    city = models.CharField(max_length=64, blank=True, default='')
    state = models.CharField(max_length=64, blank=True, default='')
    zip = models.CharField(max_length=8, blank=True, default='')
    county = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        return f'{self.address} {self.city} {self.state} {self.zip}'
