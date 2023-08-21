from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from oauth.forms import RegistrationUserForm, AuthenticationUserForm


def register_view(request):
    if request.method == "POST":
        form = RegistrationUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegistrationUserForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationUserForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")

    else:
        form = AuthenticationUserForm()
        return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'home.html')
