from django.contrib import admin
from client.models import Client, ClientAddress
from agency.admin import AgencyClientInline


admin.site.register(ClientAddress)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'middle_name', 'last_name', 'address')

    inlines = (AgencyClientInline, )

    def get_queryset(self, request):
        return Client.objects.for_user(request.user)
