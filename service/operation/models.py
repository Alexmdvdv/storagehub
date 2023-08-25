import uuid
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator


def user_directory_path(instance, filename):
    unique_filename = f'{uuid.uuid4()}.{filename.split(".")[-1]}'
    return unique_filename


class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to=user_directory_path,
                            validators=[FileExtensionValidator(allowed_extensions=["py"])])
    is_new = models.BooleanField(default=True)
    is_changed = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
