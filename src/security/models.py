from django.db import models
from agency.models import Agency
from program.models import Program


class SecurityGroup(models.Model):
    class Meta:
        db_table = 'security_group'
        ordering = ['name']
        verbose_name_plural = 'Security Groups'

    name = models.CharField(max_length=64)

    responses = models.BooleanField(default=False, verbose_name='Access Responses',
                                    help_text='Grants access to responses created by any of the agencies within the security group')
    enrollments = models.BooleanField(default=False, verbose_name='Access Client enrollment data')
    referrals = models.BooleanField(default=False, verbose_name='Access Client referral data')
    programs = models.ManyToManyField(Program, related_name='security_groups')
    agencies = models.ManyToManyField(Agency, related_name='security_groups')

    def __str__(self):
        return self.name


class SecurityGroupAgencyConfig(models.Model):
    # unused
    class Meta:
        db_table = 'security_group_agency_config'

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    security_group = models.ForeignKey(SecurityGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.agency.name}@{self.security_group.name}"
