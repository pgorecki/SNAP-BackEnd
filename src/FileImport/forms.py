from django.forms import ModelForm
from .models import FileImport


class FileImportForm(ModelForm):
    class Meta:
        model = FileImport
        fields = (
            "ftype",
            "xls_file",
        )
