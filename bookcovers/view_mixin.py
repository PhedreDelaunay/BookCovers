from bookcovers.pagers import AuthorPager
from bookcovers.pagers import ArtistPager
from bookcovers.pagers import BookPager

from bookcovers.cover_querys import CoverQuerys
from bookcovers.models import Artists
from bookcovers.models import Artworks

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
        return book_pager

class AuthorMixin(TopLevelPagerMixin):
    top_level_menu = "authors"
    pager_path = "author"

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value