from django import forms


class XlsUploadForm(forms.Form):
    xls_file = forms.FileField()
