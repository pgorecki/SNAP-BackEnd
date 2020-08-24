from rest_framework import serializers
from drf_writable_nested.serializers import NestedCreateMixin, NestedUpdateMixin
from core.serializers import ObjectSerializer, CreatedByReader
from .models import Client, ClientAddress


class ClientAddressReader(ObjectSerializer):
    class Meta:
        model = ClientAddress
        fields = ('object', 'street', 'city', 'state', 'zip', 'county')


class ClientAddressWriter(ObjectSerializer):
    class Meta:
        model = ClientAddress
        fields = ('street', 'city', 'state', 'zip', 'county')


class ClientReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)
    address = ClientAddressReader()

    class Meta:
        model = Client
        fields = ('id', 'object', 'first_name', 'middle_name', 'last_name',
                  'dob', 'ssn', 'address', 'created_at', 'modified_at', 'created_by')

    def __init__(self, *args, **kwargs):
        if len(args):
            view = kwargs['context']['view']
            request = kwargs['context']['request']
            user = request.user
            if view.action == 'list':
                clients = args[0]
                for client in clients:
                    self.filter_client_data(client, user)
            if view.action == 'retrieve':
                self.filter_client_data(args[0], user)
        return super().__init__(*args, **kwargs)

    def filter_client_data(self, client, user):
        agency = user.profile.agency
        if agency.agency_clients.filter(client=client).exists() or client.created_by.profile.agency == agency:
            """ grant access to all fields """
            pass
        else:
            client.dob = None
            client.ssn = None
            client.address = None


class ClientWriter(NestedCreateMixin, NestedUpdateMixin, ObjectSerializer):
    address = ClientAddressWriter(required=False)

    class Meta:
        model = Client
        fields = ('first_name', 'middle_name', 'last_name', 'dob', 'ssn', 'address')
