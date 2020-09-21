from core.serializers import ObjectSerializer
from .models import Agency


class AgencyReader(ObjectSerializer):
    class Meta:
        model = Agency
        fields = ("id", "object", "name")
