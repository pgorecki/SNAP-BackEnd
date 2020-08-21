from rest_framework import serializers
from drf_yasg import openapi
from django.apps import apps
from django.utils.module_loading import import_string
from django.contrib.auth.models import User


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to serialize generic relations
    """
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "SourceObject",
            "properties": {
                "id": openapi.Schema(
                     title="source object id",
                     type=openapi.TYPE_STRING,
                ),
                "type": openapi.Schema(
                    title="source object type, (Client, User, ...)",
                    type=openapi.TYPE_STRING,
                ),
                "...": openapi.Schema(
                    title="other fields of source object",
                    type=openapi.TYPE_STRING,
                    read_only=True,
                )
            },
            "required": ["subject", "body"],
        }

    MODELS = {
        'Client': ('client', 'Client'),
        # 'Enrollment': ('program', 'Enrollment'),
    }

    def to_representation(self, object):
        object_app = object._meta.app_label
        object_name = object._meta.object_name
        serializer_module_path = f'{object_app}.serializers.{object_name}Reader'
        serializer_class = import_string(serializer_module_path)
        data = serializer_class(object).data
        return data

    def to_internal_value(self, data):
        app_name, model_name = self.MODELS.get(data['type'], (None, data['type']))
        if app_name is None:
            for model in apps.get_models():
                if model.__name__ == model_name:
                    break
        else:
            model = apps.get_model(app_name, model_name)
        return model.objects.get(pk=data['id'])


class ObjectSerializer(serializers.ModelSerializer):
    object = serializers.SerializerMethodField()

    def get_object(self, object):
        return object._meta.object_name


class CreatedByReader(ObjectSerializer):
    class Meta:
        model = User
        fields = ('id', 'object', 'first_name', 'last_name')


class UserReader(CreatedByReader):
    pass
