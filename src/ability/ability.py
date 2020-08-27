import inspect
from django.apps import apps


class Ability:
    def __init__(self, user):
        self.user = user
        self.abilities = []

    def declare_can(self, action, model, **kwargs):
        if type(model) is str:
            model = apps.get_model(model)
        self.abilities.append({
            'type': 'can',
            'action': action,
            'model': model,
            'conditions': kwargs,
        })

    def declare_cannot(self, action, model, **kwargs):
        if type(model) is str:
            model = apps.get_model(model)

        self.abilities.append({
            'type': 'cannot',
            'action': action,
            'model': model,
            'conditions': kwargs,
        })

    def evaluate_model(self, action, model):
        can_count = 0
        cannot_count = 0
        model_abilities = filter(lambda c: c['model'] == model and c['action'] == action, self.abilities)
        for c in model_abilities:
            if c['type'] == 'can':
                can_count += 1
            if c['type'] == 'cannot':
                cannot_count += 1

        if cannot_count > 0:
            return False
        if can_count == 0:
            return False
        return True

    def evaluate_instance(self, action, instance):
        model = instance._meta.model
        model_abilities = filter(lambda c: c['model'] == model and c['action'] == action, self.abilities)
        can_query_set = model.objects.all().filter(pk=instance.id)
        for c in model_abilities:
            if c['type'] == 'can':
                can_query_set = can_query_set.filter(**c.get('conditions', {}))

            if c['type'] == 'cannot':
                can_query_set = can_query_set.exclude(**c.get('conditions', {}))

        # print(('+', can_query_set.all()))

        return can_query_set.count() > 0

    def can(self, action, model_or_instance) -> bool:
        if inspect.isclass(model_or_instance):
            return self.evaluate_model(action, model_or_instance)
        else:
            return self.evaluate_instance(action, model_or_instance)
