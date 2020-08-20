from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from model_utils.models import (
    UUIDModel,
    AutoCreatedField,
    AutoLastModifiedField,
    TimeStampedModel as TSM
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from .validation import ModelValidationMixin


class ObjectRoot(ModelValidationMixin, UUIDModel):
    class Meta:
        abstract = True
        ordering = ['created_at']

    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True)
    created_at = AutoCreatedField(_('created_at'))
    modified_at = AutoLastModifiedField(_('modified_at'))


class TimeStampedModel(TSM):
    class Meta:
        abstract = True
        ordering = ['created_at']

    created_at = AutoCreatedField(_('created_at'))
    modified_at = AutoLastModifiedField(_('modified_at'))
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True)


class UserProfile(models.Model):
    class Meta:
        db_table = 'user_profile'
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    agency = models.ForeignKey(
        'agency.Agency', related_name='user_profiles', on_delete=models.PROTECT, blank=True, null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
