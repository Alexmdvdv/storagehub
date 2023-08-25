from django import forms

from operation.models import FileModel


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ('file',)
        labels = {
            'file': 'Файл'
        }

