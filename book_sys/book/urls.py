from django.urls import path
from .views import *

App_Name = 'book'
urlpatterns = [
    path("", Main.as_view(), name="all"),
    path('new/',CreateBook.as_view() , name= 'create_book'),
    path('book/<int:pk>/',DetailBook.as_view() , name='detail_book'),
    path("register/",register_request, name="register"),
]
