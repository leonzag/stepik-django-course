from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Comment


class FeedBackForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "name",
                "placeholder": "Ваше имя",
            }
        ),
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "placeholder": "Ваша почта",
            }
        ),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "subject",
                "placeholder": "Тема",
            }
        ),
    )
    message = forms.CharField(
        max_length=200,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "message",
                "rows": 2,
                "placeholder": "Ваше сообщение",
            }
        ),
    )


class SignInForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "inputUsername",
                "placeholder": "Имя пользователя",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mt-2",
                "id": "inputPassword",
                "placeholder": "Пароль",
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        if not User.objects.filter(username__iexact=username):
            raise forms.ValidationError("Пользователь с таким именем не найден")
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Неверный пароль")


class SignUpForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "inputUsername",
                "placeholder": "Имя пользователя",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mt-2",
                "id": "inputPassword",
                "placeholder": "Пароль",
            }
        ),
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mt-2",
                "id": "ReInputPassword",
                "placeholder": "Повторите пароль",
            }
        ),
    )

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["repeat_password"]

        if User.objects.filter(username__iexact=username):
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            password=self.cleaned_data["password"],
        )
        user.save()
        return user


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }
