from django.urls import path
from bookcovers.views import AuthorList

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    path('authors/', AuthorList.as_view()),


]
