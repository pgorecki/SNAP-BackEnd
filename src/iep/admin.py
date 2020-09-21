from django.contrib import admin
from .models import ClientIEP, ClientIEPEnrollment, JobPlacement


class ClientIEPEnrollmentInline(admin.StackedInline):
    model = ClientIEPEnrollment


@admin.register(ClientIEP)
class ClientIEPAdmin(admin.ModelAdmin):
    inlines = (ClientIEPEnrollmentInline,)


admin.site.register(JobPlacement)
