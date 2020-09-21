from rest_framework import serializers


class ApplicationValidationError(serializers.ValidationError):
    """
    class for application-level validation errors
    """

    pass
