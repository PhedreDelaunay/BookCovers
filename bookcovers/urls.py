from django.urls import path
from bookcovers.views import AuthorList
from bookcovers.views import ArtistList


from . import views

app_name = 'bookcovers'
urlpatterns = [
    path('', views.index, name='index'),
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    path('authors/', AuthorList.as_view(), name='authors'),
    path('artists/', ArtistList.as_view(), name='artists'),
]

# https://docs.djangoproject.com/en/2.0/intro/tutorial01/
# path() argument: name
# Naming your URL lets you refer to it unambiguously from elsewhere in Django, especially from within templates. 
# This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.
# the 'name' value as called by the {% url %} template tag

