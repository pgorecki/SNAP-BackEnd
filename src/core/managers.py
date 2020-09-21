from django.db import models


class AgencyObjectManager(models.Manager):
    def for_user(self, user):
        if user.is_superuser:
            return super().get_queryset()
        if not hasattr(user, "profile"):
            return self.none()
        # compare agency of object author == agency of the current user
        return (
            super()
            .get_queryset()
            .filter(created_by__profile__agency=user.profile.agency)
        )
