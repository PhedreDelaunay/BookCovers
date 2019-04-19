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

    @property
    def book_pager(self):
        return self._book_pager

    @book_pager.setter
    def book_pager(self, value):
        self._book_pager = value