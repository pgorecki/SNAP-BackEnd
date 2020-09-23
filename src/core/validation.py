from django.db.models.signals import ModelSignal
from core.exceptions import ApplicationValidationError

model_validation = ModelSignal(
    providing_args=["instance", "raw", "using", "update_fields"], use_caching=True
)


class ModelValidationMixin:
    def clean(self):
        model_validation.send(sender=self.__class__, instance=self)


def validate_fields_with_abilities(ability, data, **kwargs):
    for field, action in kwargs.items():
        if field in data and not ability.can(action, data[field]):
            raise ApplicationValidationError({field: [f"Cannot {action} {field} {data[field]}"]})
