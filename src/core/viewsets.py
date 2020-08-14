from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType


class ModelViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        """
        This method will be used by all non-overriden operations
        """
        if self.action in ['create', 'update', 'partial_update']:
            serializer_class = self.get_write_serializer_class()
        else:
            # list, retrieve
            serializer_class = self.get_read_serializer_class()

        assert serializer_class is not None
        return serializer_class

    def get_read_serializer_class(self):
        read_serializer_class = getattr(
            self, 'read_serializer_class', None) or super().get_read_serializer_class()
        return read_serializer_class

    def get_write_serializer_class(self):
        write_serializer_class = getattr(
            self, 'write_serializer_class', None) or super().get_write_serializer_class()
        return write_serializer_class

    def get_read_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for serializing output.
        """
        reader_class = self.get_read_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return reader_class(*args, **kwargs)

    def get_write_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input.
        """
        writer_class = self.get_write_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return writer_class(*args, **kwargs)

    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        writer = self.get_write_serializer(data=request.data)
        writer.is_valid(raise_exception=True)
        if hasattr(self, 'validate_create'):
            self.validate_create(request, writer.validated_data)
        else:
            self.validate(request, writer.validated_data, 'create')
        self.perform_create(writer)
        instance = writer.instance
        headers = self.get_success_headers(writer.data)
        reader = self.get_read_serializer(instance)
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=ADDITION,
            change_message=f"Added via {self.get_view_name()}.",
        )
        request.logger.set_context(
            data=writer.validated_data,
            instance=instance,
        ).info(f'{instance.__class__.__name__} created')
        return Response(reader.data, status=status.HTTP_201_CREATED, headers=headers)

    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        writer = self.get_write_serializer(self.get_object(), data=request.data, partial=partial)
        writer.is_valid(raise_exception=True)
        if hasattr(self, 'validate_update'):
            self.validate_update(request, writer.validated_data)
        else:
            self.validate(request, writer.validated_data, 'update')
        self.perform_update(writer)
        instance = writer.instance

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=CHANGE,
            change_message=f"Changed via {self.get_view_name()}.",
        )
        request.logger.set_context(
            data=writer.validated_data,
            instance=instance,
        ).info(f'{instance.__class__.__name__} changed')

        reader = self.get_read_serializer(instance)
        return Response(reader.data)

    """
    Delete model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response = super().destroy(request, *args, **kwargs)
        print(response)
        LogEntry.objects.log_action(
            user_id=request.user.pk,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.pk,
            object_repr=str(instance),
            action_flag=DELETION,
            change_message=f"Deleted via {self.get_view_name()}.",
        )
        request.logger.set_context(
            instance=instance,
        ).info(f'{instance.__class__.__name__} deleted')
        return response

    def validate(self, request, data, action):
        """
        Raise exception in case of application-level error:

        raise ApplicationValidationError({'some_field': ['Some error message']})
        """
