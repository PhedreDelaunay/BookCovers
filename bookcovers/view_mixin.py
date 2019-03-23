from django.shortcuts import get_object_or_404

from bookcovers.pagers import AuthorPager
from bookcovers.pagers import ArtistPager
from bookcovers.pagers import BookPager

from bookcovers.cover_querys import CoverQuerys
from bookcovers.models import Author
from bookcovers.models import Artists
from bookcovers.models import Artworks
from bookcovers.models import Books

# https://reinout.vanrees.org/weblog/2011/08/24/class-based-views-walkthrough.html
# the view is available in the template for generic class based views
# so can provide data as attributes rather than manipulating context

# Base mixin used by all web pages to provide html title
class TitleMixin():
    @property
    def web_title(self):
        return self._web_title

    @web_title.setter
    def web_title(self, value):
        self._web_title = value

class TopLevelPagerMixin(TitleMixin):

    @property
    def the_pager(self):
        return self._the_pager

    @the_pager.setter
    def the_pager(self, value):
        self._the_pager = value

class ArtistMixin(TopLevelPagerMixin):
    top_level_menu = "artists"
    pager_path="artist"

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        print (f"artist_setter: value is {value}")
        self._artist = value

    @property
    def artwork(self):
        return self._artwork

    @artwork.setter
    def artwork(self, value):
        print(f"artwork_setter: value is {value}")
        self._artwork = value

    @property
    def book_pager(self):
        return self._book_pager

    @book_pager.setter
    def book_pager(self, value):
        self._book_pager = value

    def get_artwork(self, artwork_id):
        self.artwork = get_object_or_404(Artworks, artwork_id=artwork_id)
        self.web_title = self.artwork.name
        print (f"ArtworkMixin: get_artwork: artwork_id={artwork_id}")

    def create_top_level_pager(self, artist_id=None, name=None, slug=None):
        artist_pager = ArtistPager(self.request,  artist_id=artist_id, name=name, slug=slug)
        return artist_pager

    def create_book_pager(self):
        # book cover pager
        page = self.request.GET.get('page')
        print(f"ArtworkMixin: create_book_pager - page is '{page}'")

        pager = BookPager(page=page, item_id=self.artwork.pk)
        book_pager = pager.pager(book_cover_query=CoverQuerys.artist_cover_list,
                                 item_id_key="artwork_id",
                                 item_model=Artworks,
                                 subject_id_key='artist_id',
                                 subject_model=Artists)
        self.artwork = pager.get_entry()
        print (f"ArtworkMixin: create_book_pager: artwork_id={self.artwork.pk}")
        return book_pager

class AuthorMixin(TopLevelPagerMixin):
    top_level_menu = "authors"
    pager_path = "author"

    # @property
    # def author(self):
    #     return self._author
    #
    # @author.setter
    # def author(self, value):
    #     self._author = value

    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, value):
        print(f"book_setter: value is {value}")
        self._book = value

    def get_book(self, book_id):
        self.book = get_object_or_404(Books, pk=book_id)
        self.web_title = self.book.title
        self.author_id = self.book.author_id
        print (f"AuthorkMixin: get_book: book_id={book_id}")

    def create_top_level_pager(self, author_id):
        author_pager = AuthorPager(self.request, author_id=author_id)
        return author_pager

    def create_book_pager(self):
        # book title pager
        page = self.request.GET.get('page')
        print(f"AuthorMixin: create_book_pager - page is '{page}'")

        pager = BookPager(page=page, item_id=self.book_id)
        book_pager = pager.pager(book_cover_query=CoverQuerys.books_for_author,
                                 item_id_key="book_id",
                                 item_model=Books,
                                 subject_id_key='author_id',
                                 subject_model=Author)
        self.book = pager.get_entry()
        self.book_id = self.book.pk
        print (f"AuthorkMixin: create-book_pager: book_id={self.book.pk}")
        return book_pager