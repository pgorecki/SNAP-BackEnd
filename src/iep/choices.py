from django.db import models


class IEPStatus(models.TextChoices):
    AWAITING_APPROVAL = "awaiting_approval", "Awaiting approval"
    IN_ORIENTATION = "in_orientation", "In orientation"
    IN_PLANNING = "in_planning", "In planning"
    IN_PROGRESS = "in_progress", "In progress"
    NOT_ELIGIBLE = "not_eligible", "Not eligible"
    ENDED = "ended", "Ended"


class IEPProgramStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    ENROLLED = "enrolled", "Enrolled"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"
