from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="玩家名稱")
    email = forms.EmailField(label="電子信箱", required=True)
    password1 = forms.CharField(label="密碼", widget=forms.PasswordInput)
    password2 = forms.CharField(label="確認密碼", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("這個電子信箱已經被註冊。")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="電子信箱")
    password = forms.CharField(label="密碼", widget=forms.PasswordInput)
    remember = forms.BooleanField(label="記住我", required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            return cleaned_data

        user = User.objects.filter(email=email.lower()).first()

        if user is None:
            raise forms.ValidationError("帳號或密碼不正確。")

        authenticated_user = authenticate(
            username=user.username,
            password=password,
        )

        if authenticated_user is None:
            raise forms.ValidationError("帳號或密碼不正確。")

        cleaned_data["user"] = authenticated_user
        return cleaned_data
