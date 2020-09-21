import factory
from .models import Survey, Question


class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Survey

    name = factory.Sequence(lambda n: f"Survey {n}")
    definition = {
        "items": [],
    }


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    title = factory.Sequence(lambda n: f"Question {n}")
