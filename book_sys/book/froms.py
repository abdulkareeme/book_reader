from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from .models import *

class BookForm(ModelForm):
    class Meta :
        model = Book
        fields =['title' , 'preview' , 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'preview' : forms.TextInput(attrs={'class':'form-control'}),
            'title' : forms.TextInput(attrs={'class':'form-control'})
        }


class UploadFile(forms.Form):
    upfile = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))

class UserCreateForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username","email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email= self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileForm(ModelForm):
    class Meta :
        model = Profile
        fields = ['account_type']
    