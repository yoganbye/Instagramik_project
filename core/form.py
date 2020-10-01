from django import forms
from core.models import Post, Comment
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):#форма создания юзера
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Пароль', 'class' : 'form-control'
        })
    )

    password2 = forms.CharField(
        label="Подтверждение пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Подтвердите пароль', 'class' : 'form-control'
        }),
        help_text='Введите тот же пароль, что и выше'
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            'username' : forms.TextInput(attrs={
                'class' : 'form-control', 'placeholder' : 'Username'
            }),
            'email' : forms.EmailInput(attrs={
                'class' : 'form-control', 'placeholder' : 'email',
                'authofocus' : True
            })
        }


class LoginForm(AuthenticationForm):#form логина
    username = UsernameField(widget=forms.TextInput(attrs={
            'autofocus' : True, 'placeholder' : 'Username', 'class' : 'form-control'
        })
    )

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Пароль', 'class' : 'form-control'
        })
    )

    error_messages = {
        'invalid_login' : 'Введен неправильный логин или пароль.'
    }


class PostForm(forms.ModelForm):#Наследуемся от ModelsForm, но можно и от других классов

    class Meta:
        # Модель:
        model = Post
        # Поля модели:
        fields = ['description', 'image']
        labels = {
            'description' : 'Описание поста',
            'image' : 'Выберите файл'
        }#описание поля - лейбл

        widgets = {
            'description' : forms.Textarea(attrs={
                'class' : 'form-control', 'placeholder' : 'Описание поста'
            }),#Textarea - поле куда писать; attr - параметры чего-то
            'image' : forms.ClearableFileInput(attrs={
                'type' : 'file', 'class' : 'form-control-file'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widget = {
            'text' : forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': ' Текст комментария'
                })
        }