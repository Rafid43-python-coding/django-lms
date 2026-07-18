from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from email_service.utils import send_welcome_email
from .forms import RegisterForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            

            send_welcome_email(user)

            messages.success(request, "Registration successful! Please login.")
            return redirect("login")
        else:
            print(form.errors) # Add this line
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("home")

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("home")
