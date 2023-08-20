from django.db import models
from django.core.validators import FileExtensionValidator

from oauth.models import User


class FileModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/', validators=[FileExtensionValidator(allowed_extensions=["py"])])
    is_new = models.BooleanField(default=True)
    is_changed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
