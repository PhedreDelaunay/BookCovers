from django.urls import path
# from bookcovers.artist.views import ArtistList
# from bookcovers.artist.views import ArtistArtworks
# from bookcovers.artist.views import Artwork
# from bookcovers.artist.views import Artworks
# from bookcovers.artist.views import ArtistSets
# from bookcovers.artist.views import ArtworkEdition
# from bookcovers.artist.views import ArtworkSet
# from bookcovers.artist.views import ArtworkSetEdition
# from bookcovers.artist.views import ArtworkSetEditions
#
# from bookcovers.author.views import AuthorList
# from bookcovers.author.views import AuthorBooks
# from bookcovers.author.views import Book
# from bookcovers.author.views import Books
# from bookcovers.author.views import AuthorSets
# from bookcovers.author.views import BookEdition
# from bookcovers.author.views import SetEdition
# from bookcovers.author.views import SetEditions

from .artist.views import *
from .author.views import *
from bookcovers.views import PrintHistory

from bookcovers.views import Edition
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
    # ex: /bookcovers/author/Robert%20Heinlein/
    path('author/<name>/', AuthorBooks.as_view(), name='author_books'),
    # ex: /bookcovers/author/Ray%20Bradbury/sets/
    path('author/<name>/sets/', AuthorSets.as_view(), name='author_sets'),
    # ex: /bookcovers/artists/
    path('artists/', ArtistList.as_view(), name='artists'),
    # ex: /bookcovers/artist/6/
    path('artist/<int:artist_id>/', ArtistArtworks.as_view(), name='artist_artworks'),
    # ex: /bookcovers/artist/Jim-Burns/
    path('artist/<slug:slug>/',  ArtistArtworks.as_view(), name='artist_artworks'),
    # ex: /bookcovers/artist/Jim%20Burns/
    path('artist/<name>/', ArtistArtworks.as_view(), name='artist_artworks'),
    # ex: /bookcovers/artist/Bruce%20Pennington/sets/
    path('artist/<name>/sets/', ArtistSets.as_view(), name='artist_sets'),
    # ex: /bookcovers/book/467/
    path('book/<int:book_id>/', Book.as_view(), name='book'),
    # ex: /bookcovers/book/Machineries%20Of%20Joy/ - not yet implemented
    path('book/<title>/',  Book.as_view(), name='book'),
    # ex: /bookcovers/books/7/
    path('books/<int:book_id>/', Books.as_view(), name='books'),
    # ex: /bookcovers/book/edition/6/
    path('book/edition/<int:edition_id>/', BookEdition.as_view(), name="book_edition"),
    # /bookcovers/book/set/detail/3/
    path('book/set/detail/<int:set_id>/', BookSetDetail.as_view(), name="book_set_detail"),
    # /bookcovers/book/set/list/3/
    path('book/set/list/<int:set_id>/', BookSetList.as_view(), name="book_set_list"),
    # ex: /bookcovers/book/set/edition/6/
    path('book/set/edition/<int:edition_id>/', BookSetEdition.as_view(), name="set_edition"),
    # ex: /bookcovers/book/set/editions/6/
    path('book/set/editions/<int:edition_id>/', BookSetEditions.as_view(), name="set_editions"),
    # ex: /bookcovers/artwork/12/
    path('artwork/<int:artwork_id>/', Artwork.as_view(), name='artwork'),
    # ex: /bookcovers/artworks/6/
    path('artworks/<int:artwork_id>/', Artworks.as_view(), name='artworks'),
    # ex: /bookcovers/artwork/edition/7/
    path('artwork/edition/<int:edition_id>/', ArtworkEdition.as_view(), name="artwork_edition"),
    # /bookcovers/artwork/set/detail/3/
    path('artwork/set/detail/<int:set_id>/', ArtworkSetDetail.as_view(), name="artwork_set_detail"),
    # /bookcovers/artwork/set/list/3/
    path('artwork/set/list/<int:set_id>/', ArtworkSetList.as_view(), name="artwork_set_list"),
    # ex: /bookcovers/artwork/set/edition/6/
    path('artwork/set/edition/<int:edition_id>/', ArtworkSetEdition.as_view(), name="artwork_set_edition"),
    # ex: /bookcovers/artwork/set/editions/6/
    path('artwork/set/editions/<int:edition_id>/', ArtworkSetEditions.as_view(), name="artwork_set_editions"),
    # ex: /bookcovers/print_run/7/
    path('print_run/<int:print_run_id>/', PrintHistory.as_view(), name="print_history"),
    # ex: /bookcovers/edition/6/
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
