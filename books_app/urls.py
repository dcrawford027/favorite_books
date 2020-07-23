from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('add_book', views.addBook),
    path('logout', views.logout),
    path('like_book/<int:book_id>', views.likeBook),
    path('books/<int:book_id>', views.showBook),
    path('update_book', views.updateBook),
    path('delete_book', views.deleteBook),
]