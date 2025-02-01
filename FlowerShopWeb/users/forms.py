from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class CustomUserRegisterForm(UserCreationForm):
    # email = forms.EmailField()

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'password1', 'password2']


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

class UserChangeForm(forms.ModelForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'phone']
        widgets = {
            'password': forms.PasswordInput(),  # Если вы хотите также изменить пароль
        }