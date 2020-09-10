from django.db import models


class ServiceType(models.TextChoices):
    ATTENDANCE = 'attendance', 'Attendance'
    TIME_BASED = 'time_based', 'Time based'
    DIRECT = 'direct', 'Direct'
