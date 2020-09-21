from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from agency.models import Agency
from .models import Eligibility, ClientEligibility, EligibilityQueue

# Register your models here.


@admin.register(EligibilityQueue)
class EligibilityQueueAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "requestor", "status", "created_at", "resolved_by")


@admin.register(ClientEligibility)
class ClientEligibilityAdmin(SimpleHistoryAdmin):
    list_display = ("id", "client", "status", "created_at")


@admin.register(Eligibility)
class ProgramAdmin(admin.ModelAdmin):
    class AgenciesInline(admin.TabularInline):
        model = Agency.eligibility.through
        exclude = ["created_by"]

    inlines = (AgenciesInline,)
