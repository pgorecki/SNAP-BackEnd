from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from agency.models import Agency, AgencyClient
from .forms import XlsUploadForm


class AgencyClientInline(admin.TabularInline):
    model = AgencyClient


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [
            path('<object_id>/import-xls/', self.import_xls)
        ] + super().get_urls()

    def import_xls(self, request, object_id):
        form = XlsUploadForm()
        payload = {'form': form}
        return render(
            request, 'admin/agency/xls_import.html', payload
        )
