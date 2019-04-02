from django.urls import path
from bookcovers.views import AuthorList
from bookcovers.views import ArtistList
from bookcovers.views import AuthorBooks
from bookcovers.views import ArtistArtworks
from bookcovers.views import Artwork
from bookcovers.views import ArtworkList
from bookcovers.views import ArtworkCover
from bookcovers.views import Edition
from bookcovers.views import Book
from bookcovers.views import BookList
from bookcovers.views import BookArtistSets
from bookcovers.views import BookEdition

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
    # ex: /bookcovers/author/4/
    path('author/<int:author_id>/', AuthorBooks.as_view(), name='author_books'),
    # ex: /bookcovers/author/Robert-Heinlein/
    path('author/<slug:slug>/', AuthorBooks.as_view(), name='author_books'),
    # ex: /bookcovers/author/Robert%20Heinelein/
    path('author/<name>/', AuthorBooks.as_view(), name='author_books'),
    # ex: /bookcovers/artist/Ray%20Bradbury/sets/
    path('author/<name>/sets/', BookArtistSets.as_view(), name='book_artist_sets'),
    # ex: /bookcovers/artists/
    path('artists/', ArtistList.as_view(), name='artists'),
    # ex: /bookcovers/artist/6/
    path('artist/<int:artist_id>/', ArtistArtworks.as_view(), name='artist_artworks'),
    # ex: /bookcovers/artist/Jim-Burns/
    path('artist/<slug:slug>/',  ArtistArtworks.as_view(), name='artist_artworks'),
    # ex: /bookcovers/artist/Jim%20Burns/
    path('artist/<name>/', ArtistArtworks.as_view(), name='artist_artworks'),
    # ex: /bookcovers/book/467/
    path('book/<int:book_id>/', Book.as_view(), name='book'),
    # ex: /bookcovers/book/Machineries%20Of%20Joy/ - not yet implemented
    path('book/<title>/',  Book.as_view(), name='book'),
    # ex: /bookcovers/books/7/
    path('books/<int:book_id>/', BookList.as_view(), name='book_list'),
    # ex: /bookcovers/book/edition/6/
    path('book/edition/<int:edition_id>/', BookEdition.as_view(), name="book_edition"),
    # ex: /bookcovers/artwork/12/
    path('artwork/<int:artwork_id>/', Artwork.as_view(), name='artwork'),
    # ex: /bookcovers/artworks/6/
    path('artworks/<int:artwork_id>/', ArtworkList.as_view(), name='artwork_list'),
    # ex: /bookcovers/artwork/covers/7/
    path('artwork/cover/<int:edition_id>/', ArtworkCover.as_view(), name="artwork_cover"),
    # ex: /bookcovers/edition/6
    path('edition/<pk>/', Edition.as_view(), name="edition"),
    #path('edition/<int:edition_id>/', views.book_cover_detail, name="edition"),
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

# thinking of better names
# all_artists, all_covers_for_artist, all_books_for_artwork (dune and stigma) or all_artworks_by_artist_for_title (2 versions doona)
# all_authors, all_books_for_author, all_artworks_for_book
