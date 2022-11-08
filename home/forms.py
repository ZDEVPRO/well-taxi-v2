from django.contrib.auth.forms import UserCreationForm
from home.models import *
from django import forms
from django.forms import TextInput, Textarea


class NewUserForm(UserCreationForm):
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Ism'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiya'}),
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'Foydalanuvchi nomi'}),
            'phone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefon raqam'}),
            'password1': TextInput(attrs={'class': 'form-control', 'placeholder': 'Yangi parol'}),
            'password2': TextInput(attrs={'class': 'form-control', 'placeholder': 'Parolni takrorlang'}),
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user
