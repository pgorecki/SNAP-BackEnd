from django.db import models


class ProgramObjectManager(models.Manager):
    def for_user(self, user):
        if user.is_superuser:
            return super().get_queryset()
        if not hasattr(user, 'profile'):
            return self.none()

        return user.profile.agency.programs.order_by('created_at').all()


class AgencyProgramConfigObjectManager(models.Manager):
    def for_user(self, user):
        if user.is_superuser:
            return super().get_queryset()
        if not hasattr(user, 'profile'):
            return self.none()

        # return all all configs where config.agency == user's agency
        return super().get_queryset().filter(agency=user.profile.agency)


class EligibilityObjectManager(AgencyProgramConfigObjectManager):
    pass


class EnrollmentObjectManager(AgencyProgramConfigObjectManager):
    pass
