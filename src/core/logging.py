import uuid
import logging
import os
from itertools import chain
from django.db import models
from django.conf import settings


logger = logging.getLogger("django.app")


def instance_to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        if hasattr(f, "value_from_object"):
            data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        if hasattr(f, "value_from_object"):
            data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


class RequestLogger:
    def __init__(self, request, **kwargs):
        self.request = request
        self.kwargs = kwargs
        self.correlation_id = kwargs.get("correlation_id", uuid.uuid4())
        self.context = {}

    def set_context(self, **kwargs):
        self.context = kwargs
        return self

    def get_extra(self, clear_context=True):
        extra = {
            "correlation_id": self.correlation_id,
            "config": os.environ.get("DJANGO_CONFIGURATION"),
            "build_version": settings.BUILD_VERSION,
            "build_date": settings.BUILD_DATE,
        }

        if "view" in self.kwargs:
            extra["view"] = self.kwargs["view"]

        # add user data
        try:
            extra["user"] = {
                "id": self.request.user.id,
                "username": self.request.user.username,
            }
        except Exception as err:
            extra["user"] = str(err)

        for key, value in self.context.items():
            if isinstance(value, models.Model):
                extra[key] = instance_to_dict(value)
            else:
                extra[key] = value
        if clear_context:
            self.context = {}
        return extra

    def debug(self, *args, **kwargs):
        logger.debug(*args, **kwargs, extra=self.get_extra())

    def info(self, *args, **kwargs):
        logger.info(*args, **kwargs, extra=self.get_extra())

    def warning(self, *args, **kwargs):
        logger.warning(*args, **kwargs, extra=self.get_extra())

    def error(self, *args, **kwargs):
        logger.error(*args, **kwargs, extra=self.get_extra())
