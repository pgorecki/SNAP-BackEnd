from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib import admin
from survey.models import Survey, Question, Response, Answer
from .forms import SurveyAdminForm


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question


class AnswersInline(admin.TabularInline):
    model = Answer


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    inlines = (AnswersInline, )


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'id', 'usage_count')


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    form = SurveyAdminForm
