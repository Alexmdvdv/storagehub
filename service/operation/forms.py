from django import forms

from operation.models import FileModel


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ('file_path',)
        labels = {
            'file_path': 'Файл'
        }
