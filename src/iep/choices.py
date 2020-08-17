from django.db import models


class IEPStatus(models.TextChoices):
    AWAITING_APPROVAL = 'awaiting_approval', 'Awaiting approval'
    IN_PROGRESS = 'in_progress', 'In progress'
    ENDED = 'ended', 'Ended'


class IEPProgramStatus(models.TextChoices):
    PLANNED = 'planned', 'Planned'
    ENROLLED = 'enrolled', 'Enrolled'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'
