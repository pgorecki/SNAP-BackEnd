from django import forms
from .models import Survey, Question
from rest_framework import serializers


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}


class SurveyValidator:
    def __init__(self, survey, error_class):
        self.survey = survey
        self.error_class = error_class

    def validate_definition(self):
        try:
            existing_ids = set()
            existing_question_ids = set()
            for item in self.survey.get_definition_items():
                copy = without_keys(item, ["items"])
                item_id = item.get("id", None)
                if item_id:
                    if item_id in existing_ids:
                        raise self.error_class(f"Duplicated id: {copy}")
                    existing_ids.add(item_id)

                if item.get("type") == "question":
                    if "id" not in item:
                        raise forms.ValidationError(f"Missing id: {copy}")
                    if "questionId" not in item:
                        raise forms.ValidationError(f"Missing questionId: {copy}")
                    if item["questionId"] in existing_question_ids:
                        raise forms.ValidationError(f"Duplicated questionId: {copy}")
                    existing_question_ids.add(item["questionId"])

                    try:
                        Question.objects.get(pk=item["questionId"])
                    except Question.DoesNotExist:
                        raise self.error_class(f"Question does not exist: {item_id}")
        except Exception as e:
            raise self.error_class(e)


def SurveySerializerValidator(value):
    survey = Survey(**value)
    validator = SurveyValidator(survey, serializers.ValidationError)
    validator.validate_definition()
