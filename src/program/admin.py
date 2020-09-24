from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Enrollment,
    Program,
    EnrollmentService,
    EnrollmentActivity,
    EnrollmentServiceType,
)

admin.site.register(Program)


@admin.register(Enrollment)
class EnrollmentAdmin(SimpleHistoryAdmin):
    list_display = ("id", "status", "client", "program")


# @admin.register(EnrollmentService)
# class EnrollmentServiceAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "service_type",
#         "enrollment",
#         "client",
#         "agency",
#         "effective_date",
#     )
#     exclude = ("values",)

#     def agency(self, obj):
#         return obj.enrollment.program.agency

#     def client(self, obj):
#         return obj.enrollment


# admin.site.register(EnrollmentActivity)
admin.site.register(EnrollmentServiceType)
