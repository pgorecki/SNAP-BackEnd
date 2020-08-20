import rules
from django.db.models.signals import ModelSignal
from core.exceptions import ApplicationValidationError

model_validation = ModelSignal(providing_args=["instance", "raw", "using", "update_fields"],
                               use_caching=True)


class ModelValidationMixin:
    def clean(self):
        model_validation.send(sender=self.__class__, instance=self)


def validate_fields_with_rules(user, data, error_message='Not found', **kwargs):
    for field, rule_name in kwargs.items():
        assert rules.rule_exists(rule_name)
        if field in data and not rules.test_rule(rule_name, user, data[field]):
            raise ApplicationValidationError(field, [error_message])
