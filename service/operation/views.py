from django.shortcuts import render, redirect
from operation.forms import FileUploadForm
from operation.models import FileModel


def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.file_name = request.FILES['file_path'].name
            file.save()

            return redirect("succes")

    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})


def uploaded_files(request):
    user_files = FileModel.objects.filter(user=request.user)
    context = {'user_files': user_files}
    return render(request, 'uploaded_files.html', context)


def delete_file(request, file_id):
    try:
        file = FileModel.objects.get(id=file_id, user=request.user)
        file.file_path.delete()
        file.delete()
    except FileModel.DoesNotExist:
        pass

    return redirect('uploaded')


def update_file(request, file_id):
    file = FileModel.objects.get(id=file_id)

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file.file_path.delete(save=False)

            file.file_path = request.FILES['file_path']
            file.file_name = request.FILES['file_path']
            file.is_new = False

            file.save()

        return redirect("succes")
    else:
        form = FileUploadForm()

    return render(request, "update_file.html", {"form": form, "file": file})


def succes_view(request):
    return render(request, "succes.html")
