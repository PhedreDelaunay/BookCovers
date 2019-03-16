from django.urls import path
from bookcovers.views import AuthorList
from bookcovers.views import ArtistList
from bookcovers.views import AuthorBooks
from bookcovers.views import ArtistCovers
from bookcovers.views import BookCoverDetail

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
    # ex: /bookcovers/artist/Ray%20Bradbury/sets
    # do not add a / at the end of sets it will break paging; else fix subject_pager.html to handle it
    path('author/<name>/sets', views.author_book_sets, name='author_book_sets'),
    # ex: /bookcovers/artists/
    path('artists/', ArtistList.as_view(), name='artists'),
    # ex: /bookcovers/artist/6/
    path('artist/<int:artist_id>/', ArtistCovers.as_view(), name='artist_covers'),
    # ex: /bookcovers/artist/Jim-Burns/
    path('artist/<slug:slug>/',  ArtistCovers.as_view(), name='artist_covers'),
    # ex: /bookcovers/artist/Jim%20Burns/
    path('artist/<name>/', ArtistCovers.as_view(), name='artist_covers'),
    # ex: /bookcovers/book/467/
    path('book/<int:book_id>/', views.book, name='book_covers'),
    # ex: /bookcovers/book/Machineries%20Of%20Joy/ - not yet implemented
    path('book/<title>/', views.book, name='book_covers'),
    # ex: /bookcovers/author/edition/6/
    path('book/edition/<int:edition_id>/', views.book_edition, name="book_edition"),
    # ex: /bookcovers/artwork/12/
    path('artwork/<int:artwork_id>/', views.books_per_artwork, name='artwork'),
    # ex: /bookcovers/artwork/edition/6/
    path('artwork/edition/<int:edition_id>/', views.artwork_edition, name="artwork_edition"),
    # ex: /bookcovers/edition/6
    #path('edition/<pk>/', BookCoverDetail.as_view(), name="edition"),
    path('edition/<int:edition_id>/', views.book_cover_detail, name="edition"),
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
