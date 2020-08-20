from core.serializers import ObjectSerializer, CreatedByReader, UserReader
from agency.serializers import AgencyReader
from client.serializers import ClientReader
from .models import ClientIEP


class ClientIEPReader(ObjectSerializer):
    created_by = CreatedByReader()
    client = ClientReader()

    class Meta:
        model = ClientIEP
        fields = ('id', 'object', 'client', 'orientation_completed', 'status',
                  'start_date', 'end_date', 'projected_end_date',
                  'outcome', 'created_by', 'created_at', 'modified_at')


class ClientIEPWriter(ObjectSerializer):
    class Meta:
        model = ClientIEP
        fields = ('client', 'orientation_completed', 'status',
                  'start_date', 'end_date', 'projected_end_date',
                  'outcome')
