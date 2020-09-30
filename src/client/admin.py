from django.contrib import admin
from client.models import Client
from agency.admin import AgencyClientInline


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "middle_name", "last_name", "address")

    exclude = ("address",)

    inlines = (AgencyClientInline,)

    def get_queryset(self, request):
        return Client.objects.for_user(request.user)
