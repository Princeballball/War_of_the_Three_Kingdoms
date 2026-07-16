from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LoginForm, RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"註冊成功，歡迎 {user.username} 加入戰局。")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)

            if not form.cleaned_data.get("remember"):
                request.session.set_expiry(0)

            messages.success(request, f"登入成功，目前帳號：{user.username}。")
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "你已成功登出。")
    return redirect("login")
