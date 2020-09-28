from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.app_settings import swagger_settings
import rest_framework.fields
from drf_yasg import openapi
from drf_yasg.inspectors.base import FieldInspector, NotHandled


class CustomInspector(FieldInspector):
    """Provides proper swagger type for ``JSONField``."""

    def field_to_swagger_object(
        self, field, swagger_object_type, use_references, **kwargs
    ):
        SwaggerType, ChildSwaggerType = self._get_partial_types(
            field, swagger_object_type, use_references, **kwargs
        )

        if (
            isinstance(field, rest_framework.fields.ModelField)
            and swagger_object_type == openapi.Schema
        ):
            return SwaggerType(type=openapi.TYPE_OBJECT)

        return NotHandled


class CoreSwaggerAutoSchema(SwaggerAutoSchema):
    field_inspectors = [CustomInspector] + swagger_settings.DEFAULT_FIELD_INSPECTORS
