from django.contrib import admin

from operation.models import FileModel


class FileModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'is_new', 'is_changed', 'email_sent')


admin.site.register(FileModel)
