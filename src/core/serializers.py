from django.apps import apps
from django.utils.module_loading import import_string
from django.contrib.auth.models import User
from rest_framework import serializers


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to serialize generic relations
    """
    MODELS = {
        'Client': ('client', 'Client'),
    }

    def to_representation(self, object):
        object_app = object._meta.app_label
        object_name = object._meta.object_name
        serializer_module_path = f'{object_app}.serializers.{object_name}Reader'
        serializer_class = import_string(serializer_module_path)
        data = serializer_class(object).data
        return data

    def to_internal_value(self, data):
        app_name, model_name = self.MODELS.get(data['type'], (None, None))
        model = apps.get_model(app_name, model_name)
        return model.objects.get(pk=data['id'])


class ObjectSerializer(serializers.ModelSerializer):
    object = serializers.SerializerMethodField()

    def get_object(self, object):
        return object._meta.object_name


class CreatedByReader(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'id')


class UserReader(CreatedByReader):
    pass
