from rest_framework import serializers
from drf_writable_nested.serializers import NestedCreateMixin, NestedUpdateMixin
from core.serializers import ObjectSerializer, CreatedByReader
from .models import Client, ClientAddress


class ClientAddressReader(ObjectSerializer):
    class Meta:
        model = ClientAddress
        fields = ('object', 'street', 'city', 'state', 'zip', 'county')


class ClientAddressWriter(ClientAddressReader):
    pass


class ClientReader(ObjectSerializer):
    created_by = CreatedByReader(read_only=True)
    address = ClientAddressReader()

    class Meta:
        model = Client
        fields = ('id', 'object', 'first_name', 'middle_name', 'last_name',
                  'dob', 'ssn', 'address', 'created_at', 'modified_at', 'created_by')


class ClientWriter(NestedCreateMixin, NestedUpdateMixin, ObjectSerializer):
    created_by = CreatedByReader(read_only=True)
    address = ClientAddressWriter(required=False)

    class Meta:
        model = Client
        fields = ('id', 'object', 'first_name', 'middle_name', 'last_name',
                  'dob', 'ssn', 'address', 'created_at', 'modified_at', 'created_by')
