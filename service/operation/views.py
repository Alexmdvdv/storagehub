import json
from django.shortcuts import render, redirect
from operation.forms import FileUploadForm
from operation.models import FileModel
from operation.tasks import check_file


def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.name = request.FILES['file'].name
            file.save()

            return redirect("succes")

    else:
        form = FileUploadForm()

    return render(request, 'upload_file.html', {'form': form})


def uploaded_files(request):
    user_files = FileModel.objects.filter(user=request.user).order_by('-id')
    context = {'user_files': user_files}
    return render(request, 'uploaded_files.html', context)


def delete_file(request, file_id):
    try:
        file = FileModel.objects.get(id=file_id, user=request.user)
        file_path = file.file.path

        with open("logs.json", "r") as json_file:
            json_data = json.load(json_file)
            json_data = [item for item in json_data if file_path not in item]

        with open("logs.json", "w") as json_file:
            json.dump(json_data, json_file)

        if file_path:
            file.file.delete()
        file.delete()

    except FileModel.DoesNotExist:
        pass

    return redirect('uploaded')


def update_file(request, file_id):
    file = FileModel.objects.get(id=file_id)

    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file.file.delete(save=False)

            file.file = request.FILES['file']
            file.name = request.FILES['file'].name
            file.is_new = False
            file.is_changed = True

            file.save()

        return redirect("succes")
    else:
        form = FileUploadForm()

    return render(request, "update_file.html", {"form": form, "file": file})


def report_info(request, file_id):
    file = FileModel.objects.get(pk=file_id)

    with open("logs.json", "r") as json_file:
        json_data = json.load(json_file)

        result = None
        email = None
        for item in json_data:
            if file.file.path in item:
                result = item.get(file.file.path, [])
                email = item.get("email")
                break

        file_name = file.name
        context = {"result": result, "name": file_name, "email": email}

    return render(request, "report.html", context)


def succes_view(request):
    return render(request, "succes.html")
