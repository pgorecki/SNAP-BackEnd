from django import forms
from .models import Survey
from .validators import SurveyValidator


class SurveyAdminForm(forms.ModelForm):
    class Meta:
        model = Survey
        exclude = ("questions",)

    def clean(self):
        new_instance = Survey(**self.cleaned_data)
        SurveyValidator(new_instance, forms.ValidationError).validate_definition()

        return self.cleaned_data
