from django.urls import path

from operation.views import upload_file, uploaded_files, update_file, delete_file, succes_view

urlpatterns = [
    path('upload/', upload_file, name="upload"),
    path('uploaded/', uploaded_files, name="uploaded"),
    path('update/<int:file_id>/', update_file, name="update"),
    path('delete/<int:file_id>/', delete_file, name="delete"),
    path('succes/', succes_view, name="succes"),
]
