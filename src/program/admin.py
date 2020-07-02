from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from agency.models import Agency
from .models import AgencyProgramConfig, ProgramEligibility, Enrollment, Program
# Register your models here.

admin.site.register(AgencyProgramConfig)


@admin.register(ProgramEligibility)
class ProgramEligibilityAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'status', 'client', 'program')


@admin.register(Enrollment)
class EnrollmentAdmin(SimpleHistoryAdmin):
    list_display = ('id', 'status', 'client', 'program')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    class AgenciesInline(admin.TabularInline):
        model = Agency.programs.through
        exclude = ['created_by']

    inlines = (AgenciesInline, )
