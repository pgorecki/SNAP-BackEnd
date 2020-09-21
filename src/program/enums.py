from enum import Enum


class EnrollmentStatus(Enum):
    AWAITING_ENTRY = "awaiting entry"
    PLANNED = "planned"
    ENROLLED = "enrolled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXITED = "exited"


class ProgramEligibilityStatus(Enum):
    ELIGIBLE = "eligible"
    NOT_ELIGIBLE = "not eligible"
