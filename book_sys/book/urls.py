from django.urls import path
from .views import *

App_Name = 'book'
urlpatterns = [
    path("", Main.as_view(), name="all"),
    path('new_book/',CreateBook.as_view() , name= 'create_book'),
    path('book/<int:pk>/',DetailBook.as_view() , name='detail_book'),
    path("register/",register_request, name="register"),
    path("book/<int:book_pk>/<int:page_num>/",DetailPage.as_view() , name='detail_page'),
    path("accounts/profile/",ProfileView.as_view(), name='profile'),
    path('book/<int:pk>/update',OwnerUpdateBook.as_view() , name='update_book'),
    path('book/<int:pk>/delete', OwnerDeleteBook.as_view(), name='delete_book'),
    path('book/search/' , search , name='search'),
    path('accounts/profile/my_books',MyBooksView.as_view() , name='my_books'),
    path('new/new_category',CreateCategory.as_view(),name='create_category')
]
