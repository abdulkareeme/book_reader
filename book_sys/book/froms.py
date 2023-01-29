from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from .models import *

class BookForm(ModelForm):
    class Meta :
        model = Book
        fields =['title']


class UploadFile(forms.Form):
    upfile = forms.FileField()

class UserCreateForm(UserCreationForm):
    choice = [(1,'Authur'), (2,'Reader')]
    account_type= forms.IntegerField(required=True,validators=[validators.MinValueValidator(1) , validators.MaxValueValidator(2)])
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username","email", "account_type", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.account_type= self.cleaned_data["account_type"]
        if commit:
            user.save()
        return user