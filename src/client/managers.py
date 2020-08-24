from django.db import models


class ClientObjectManager(models.Manager):
    def for_user(self, user):
        if user.is_superuser:
            return super().get_queryset()
        if not hasattr(user, 'profile'):
            return self.none()
        # return all users (but serializer will hide some data)
        return super().get_queryset()
