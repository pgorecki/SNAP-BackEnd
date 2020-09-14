import json
from django.contrib import admin, messages
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.urls import path
from agency.models import Agency, AgencyClient
#from .forms import XlsUploadForm
from FileImport.forms import FileImportForm


class AgencyClientInline(admin.TabularInline):
    model = AgencyClient


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [
            path('<object_id>/import-xls/', self.import_xls)
        ] + super().get_urls()

    def import_xls(self, request, object_id):
        form = FileImportForm()

        if request.method == "POST":
            form = FileImportForm(request.POST, request.FILES)
            if not request.user.is_superuser:
                self.message_user('You must be a super user to perform this action', level=messages.ERROR)

            if form.is_valid():
                # file is saved
                object = form.save()
                result, message, other = object.inspect()

                if not result:
                    self.message_user(request, message, level=messages.ERROR)
                else:
                    run_result, rows, errors = object.run()

                    self.message_user(request, json.dumps(run_result))

            return redirect("..")

        payload = {'form': form}
        return render(
            request, 'admin/agency/xls_import.html', payload
        )
