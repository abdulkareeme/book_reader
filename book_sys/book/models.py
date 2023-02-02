from django.db import models
from django.core import validators
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    choice=[(1,'Reader'),(2,'Auther')]
    user = models.OneToOneField(User, on_delete=models.CASCADE ,related_name='profile')
    account_type = models.SmallIntegerField(choices=choice)
         
    def __str__(self):
        return self.user.username

class Book(models.Model):
    title = models.CharField(max_length=50 ,
     validators=[validators.MinLengthValidator(2,'you must input more than 1 char')])
    
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

class Page(models.Model):
    content = models.CharField(max_length=1002)
    book = models.ForeignKey( 'Book', on_delete=models.CASCADE)
    page_number = models.IntegerField()
    def __str__(self) :
        return str(self.book.title +' & page : '+ str(self.page_number))

class Read(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE , related_name= 'read_profile')
    page = models.ForeignKey('Page', on_delete=models.CASCADE , related_name='read_page')
    def __str__(self):
        return str(self.user.user.username) + '  ' + str(self.page)
    