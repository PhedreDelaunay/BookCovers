from django.urls import path
from bookcovers.views import AuthorList
from bookcovers.views import ArtistList

from . import views

# Reference:
# https://docs.djangoproject.com/en/2.1/topics/http/urls/

# Namespacing url names
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
# this is how Django knows which app view to create for a url when using the {% url %} template tag
# to point at the namespaced  view <a href="{% url 'bookcovers:view path name' question.id %}">
app_name = 'bookcovers'
urlpatterns = [
    # ex: /bookcovers/
    path('', views.index, name='index'),
    # ex: /bookcovers/authors/
    path('authors/', AuthorList.as_view(), name='authors'),
    # ex: /bookcovers/author/1/
    path('author/<int:author_id>/', views.author_books, name='author_books'),
    # ex: /bookcovers/artists/
    path('artists/', ArtistList.as_view(), name='artists'),
    # ex: /bookcovers/artist/6/
    path('artist/<int:artist_id>/', views.artist_books, name='artist_books'),
    # ex: /bookcovers/artist/Jim-Burns/
    path('artist/<slug:slug>/', views.artist_books, name='artist_books'),
    # ex: /bookcovers/artist/Jim%20Burns/
    path('artist/<name>/', views.artist_books, name='artist_books'),
    # ex: /bookcovers/book/467/
    path('book/<int:book_id>/', views.book_detail, name='book'),
]

# https://docs.djangoproject.com/en/2.0/intro/tutorial01/
# path() argument: route
# route is a string that contains a URL pattern. 
# When processing a request, Django starts at the first pattern in urlpatterns and makes its way down the list, 
# comparing the requested URL against each pattern until it finds one that matches.

# https://docs.djangoproject.com/en/2.1/intro/tutorial03/
# Using angle brackets “captures” part of the URL and sends it as a keyword argument to the view function. 
# The :author_id> part of the string defines the name that will be used to identify the matched pattern
# the <int: part is a converter that determines what patterns should match this part of the URL path.

# path() argument: view
# When Django finds a matching pattern
# it calls the specified view function with an HttpRequest object as the first argument 
# and any “captured” values from the route as keyword arguments.

# path() argument: kwargs
# Arbitrary keyword arguments can be passed in a dictionary to the target view. 

# path() argument: name
# Naming your URL lets you refer to it unambiguously from elsewhere in Django, especially from within templates. 
# This powerful feature allows you to make global changes to the URL patterns of your project while only touching a single file.
# the 'name' value as called by the {% url %} template tag

