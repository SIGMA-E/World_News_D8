from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class BaseRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_username = self.fields['username'].__dict__
        field_username['label'] = 'Никнейм'
        field_password1, field_password2 = self.fields['password1'].__dict__, self.fields['password2'].__dict__
        field_password1['label'] = 'Пароль'
        field_password2['label'] = 'Повторите пароль'

    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
