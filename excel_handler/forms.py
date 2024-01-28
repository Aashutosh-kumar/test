# excel_handler/forms.py

from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField()
