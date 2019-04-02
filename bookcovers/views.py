from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from django.views.generic import ListView
from django.views.generic import DetailView
from django.db.models import F
from django.db.models import Q
from django.template import RequestContext
from django.views.generic.detail import SingleObjectMixin

from bookcovers.models import Author
from bookcovers.models import Artists
from bookcovers.models import ArtistAkas
from bookcovers.models import Artworks
from bookcovers.models import Books
from bookcovers.models import Covers
from bookcovers.models import Editions
from bookcovers.models import Sets

from bookcovers.cover_querys import CoverQuerys
from bookcovers.record_helper import *
from bookcovers.original_raw_querys import OriginalRawQuerys

from bookcovers.pagers import ArtistPager
from bookcovers.pagers import AuthorPager
from bookcovers.pagers import BookPager

from bookcovers.view_mixin import AuthorMixin
from bookcovers.view_mixin import ArtistMixin


import math

# Create your views here.

def index(request):
    print ("index: hello page")
    return HttpResponse("Hello Django World")

# https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/
class SubjectList(ListView):
    """
    Base class for top level list (author, artist, panoramas)
    """
    num_columns=6

    # make "friendly" template context
    # https://docs.djangoproject.com/en/2.1/topics/class-based-views/generic-display/#making-friendly-template-contexts
    # in template use item_list instead of object_list
    context_object_name = 'item_list'

    # https://reinout.vanrees.org/weblog/2014/05/19/context.html
    # this is the old way of doing things as can reference view in template
    def get_context_data(self,**kwargs):
        print ("entering get_context_data")
        context = super(SubjectList,self).get_context_data(**kwargs)
        context['title'] = self.title
        print ("title is '{0}'".format(self.title))
        column_length=self.get_num_rows(self.get_queryset(), self.num_columns)
        context['column_length'] = column_length
        return context

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    def get_num_rows(self, queryset, num_columns):
        # https://docs.djangoproject.com/en/2.1/ref/models/querysets/
        # A count() call performs a SELECT COUNT(*) behind the scenes, so you should always use count() rather
        # than loading all of the record into Python objects and calling len() on the result
        # (unless you need to load the objects into memory anyway, in which case len() will be faster).
        # round up the result
        num_rows = math.ceil(queryset.count()/num_columns)
        print ("num_rows is {0}".format(num_rows))
        return num_rows


# ArtistList -> ArtistArtworks -> Artwork
# http:<host>/bookcovers/artists/
class ArtistList(SubjectList):
    template_name = 'bookcovers/artist_list.html'

    def __init__(self):
        self.title = "Artists"

    def get_queryset(self):
        queryset = CoverQuerys.artist_list()
        return queryset


# http:<host>/bookcovers/artist/<artist_id>
# http:<host>/bookcovers/artist/<artist%20name>
# http:<host>/bookcovers/artist/<artist-slug>
class ArtistArtworks(ArtistMixin, ListView):
    """
    displays list of books with covers by this artist as thumbnails
    :param request:
    one of
    :param artist_id:   ex: /bookcovers/artist/6/
    :param name:        ex: /bookcovers/artist/Jim%20Burns/
    :param slug:        ex: /bookcovers/artist/Jim-Burns/
    :return:
    """
    template_name = 'bookcovers/artist_artworks.html'
    context_object_name = 'cover_list'      # template context


    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.artist_id = kwargs.get("artist_id", None)
        self.name = kwargs.get("name", None)
        self.slug = kwargs.get("slug", None)
        self._artist = None
        print (f"in setup: artist_id={self.artist_id}")

    def set_list(self):
        # TODO
        set_list = None
        return set_list

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(artist_id=self.artist_id, name=self.name, slug=self.slug)
        # get the artist to display
        self.artist = self.the_pager.get_entry()
        self.web_title = self.artist.name
        queryset = CoverQuerys.artist_cover_list(artist=self.artist)
        return queryset


# http:<host>/bookcovers/artwork/<artwork_id>
class Artwork(ArtistMixin, DetailView):
    """
        display a single book cover using this artwork (the most common scenario)
        redirect to ArtworkList when multiple covers are returned
    """
    template_name = 'bookcovers/artwork.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.artwork_id = kwargs.get("artwork_id", None)
        self.get_artwork(self.artwork_id)

    def get_object(self, queryset=None):
        print (f"Artwork: get_object  - artist {self.artwork.artist_id}")
        self.the_pager = self.create_top_level_pager(self.artwork.artist_id)
        self.book_pager = self.create_book_pager()
        # if multiple covers are returned exception will be caught and redirect to artwork list view
        cover = Covers.objects.get(artwork_id=self.artwork.pk, flags__lt=256)
        print (f"Artwork: get_object; cover is {cover}")
        edition = get_object_or_404(Editions, edition_id=cover.edition.pk)
        return edition

    def get(self, request, **kwargs):
        try:
            return super().get(request, **kwargs)
        except Covers.MultipleObjectsReturned:
            return redirect(to='bookcovers:artwork_list', permanent=False, artwork_id=self.artwork.pk)


# http:<host>/bookcovers/artworks/<artwork_id>
class ArtworkList(ArtistMixin, ListView):
    """
        displays all book covers using the same artwork, eg
        'Dune' and 'The Three Stigmata of Palmer Eldritch' by BP
        or all book covers by same artist for the same title, eg two versions of "Decision at Doona" by BP
    """
    template_name = 'bookcovers/artwork_list.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        self.page_kwarg = "cover"
        super().setup(request, *args, **kwargs)
        self.artwork_id = kwargs.get("artwork_id", None)
        self.get_artwork(self.artwork_id)

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(artist_id=self.artwork.artist_id)
        self.book_pager = self.create_book_pager()
        print (f"ArtworkList: get_queryset artwork.name={self.artwork.name}")
        queryset = CoverQuerys.all_covers_for_artwork(self.artwork)
        return queryset


class ArtworkCover(ArtistMixin, DetailView):
    template_name = 'bookcovers/artwork_cover.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)

    def get_object(self, queryset=None):
        edition = get_object_or_404(Editions, edition_id=self.edition_id)
        print (f"ArtworkCover: artwork id is '{edition.theCover.artwork.pk}'")
        self.get_artwork(edition.theCover.artwork.pk)
        self.the_pager = self.create_top_level_pager(artist_id=self.artwork.artist_id)
        self.book_pager = self.create_book_pager()
        print(f"ArtworkCover: get_object artwork.name={self.artwork.name}")
        return edition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cover_list'] = CoverQuerys.all_covers_for_artwork(self.artwork)
        return context


# Use this for AuthorCovers but will need to provide own pager
# cos default pager assumes you are coming in from first page
# TODO refactor pagers to follow MultipleObjectMixin
# https://github.com/django/django/blob/master/django/views/generic/list.py
# /Users/tarbetn/Virtualenvs/djabbic/lib/python3.7/site-packages/django/views/generic
# http://127.0.0.1:8000/bookcovers/artwork/covers/7/
# class ArtworkCovers(ArtworkList):
#     paginate_by = 1
#     template_name = 'bookcovers/artwork_cover.html'
#
#     def setup(self, request, *args, **kwargs):
#         super().setup(request, *args, **kwargs)
#         self.edition_id = kwargs.get("edition_id", None)
#         self.edition = get_object_or_404(Editions, edition_id=self.edition_id)
#         print (f"ArtworkCovers: artwork id is '{self.edition.theCover.artwork.pk}'")
#         self.get_artwork(self.edition.theCover.artwork.pk)



# AuthorList -> AuthorBooks -> Book
# http:<host>/bookcovers/authors/
class AuthorList(SubjectList):
    template_name = 'bookcovers/author_list.html'

    def __init__(self):
        self.title = "Authors"

    def get_queryset(self):
        queryset = CoverQuerys.author_list()
        return queryset


# http:<host>/bookcovers/author/<author_id>/
# http:<host>/bookcovers/author/<author%20name>/
# http:<host>/bookcovers/author/<author-slug>/
class AuthorBooks(AuthorMixin, ListView):
    """
    displays a list of books by this author as thumbnails
    :param request:
    one of
    :param author_id:   ex: /bookcovers/author/4/
    :param name:        ex: /bookcovers/author/Robert%20Heinlein/
    :param slug:        ex: /bookcovers/author/Robert-Heinlein/
    :return:
    """
    template_name = 'bookcovers/author_books.html'
    context_object_name = 'cover_list'      # template context

    # setup is called when the class instance is created
    # note: not in 2.1, added in 2.2
    # /Users/tarbetn/Virtualenvs/djabbic/lib/python3.7/site-packages/django/views/generic/base.py
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.author_id = kwargs.get("author_id", None)
        self.name = kwargs.get("name", None)
        self.slug = kwargs.get("slug", None)
        #self._author = None
        print (f"AuthorBooks::setup: author_id='{self.author_id}', name='{self.name}', slug='{self.slug}'")

    def set_list(self):
        set_list = CoverQuerys.author_set_list(author_id=self.author.pk)
        return set_list

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(author_id=self.author_id, name=self.name, slug=self.slug)
        self.author = self.the_pager.get_entry()
        print (f"AuthorBooks:get_queryset: author is '{self.author.name}'")
        self.web_title = self.author.name
        queryset = CoverQuerys.all_covers_of_all_books_for_author(author=self.author, all=False)
        return queryset

    # def dispatch(self, request, *args, **kwargs):
    #
    #     #print(**kwargs)
    #
    #     self.author_id = kwargs['author_id']
    #     print(f"in dispatch function {self.author_id}")
    #     # needed to have an HttpResponse
    #     return super(AuthorBooks, self).dispatch(request, *args, **kwargs)


# http:<host>/bookcovers/book/<book_id>
# http:<host>/bookcovers/book/<the%20title> - not implemented
class Book(AuthorMixin, DetailView):
    """
        display a single book title selected from an author's list
        redirect to BookList when multiple covers are returned
    """
    template_name = 'bookcovers/book.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.book_id = kwargs.get("book_id", None)

    def get_object(self, queryset=None):
        # order matters, get book pager (and book) first to ascertain the author
        self.book_pager = self.create_book_pager(book_id=self.book_id)
        print (f"Book: get  - now book is {self.book_id}")
        self.the_pager = self.create_top_level_pager(author_id=self.book.author_id)
        # if multiple covers are returned exception will be caught and redirect to artwork list view
        cover = Covers.objects.get(book=self.book_id, flags__lt=256)
        print (f"Book: get_object; cover is {cover}")
        edition = get_object_or_404(Editions, edition_id=cover.edition.pk)
        return edition

    def get(self, request, **kwargs):
        try:
            return super().get(request, **kwargs)
        except Covers.MultipleObjectsReturned:
            return redirect(to='bookcovers:book_list', permanent=False, book_id=self.book_id)

# http:<host>/bookcovers/books/<book_id>
class BookList(AuthorMixin, ListView):
    """
        displays all the covers for the same book title
    """
    template_name = 'bookcovers/book_list.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.book_id = kwargs.get("book_id", None)

    def get_queryset(self):
        # order matters, get book pager (and book) first to ascertain the author
        self.book_pager = self.create_book_pager(book_id=self.book_id)
        self.the_pager = self.create_top_level_pager(author_id=self.book.author_id)
        print (f"BookList: get_queryset book.title={self.book.title}")
        queryset = CoverQuerys.all_covers_for_title(self.book)
        return queryset


class BookEdition(AuthorMixin, DetailView):
    template_name = 'bookcovers/book_edition.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)

    def get_object(self, queryset=None):
        edition = get_object_or_404(Editions, edition_id=self.edition_id)
        print (f"BookEdition: author id is '{edition.book.author_id}'")
        self.the_pager = self.create_top_level_pager(author_id=edition.book.author_id)
        self.book_pager = self.create_book_pager(book_id=edition.book.pk)
        # TODO book_pager sets self.book but this is not obvious, make more explicit
        return edition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cover_list'] = CoverQuerys.all_covers_for_title(self.book)
        print ("BookEdition: get_context")
        return context


# http:<host>/bookcovers/author/<author%20name>/sets
class BookArtistSets(AuthorMixin, ListView):
    """
    displays thumbnails of books by this author ordered in sets by artist
    """
    template_name = 'bookcovers/book_artist_sets.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.name = kwargs.get("name", None)
        print (f"BookArtistSets::setup: author={self.name}")

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(name=self.name)
        self.author = self.the_pager.get_entry()
        self.web_title = self.author.name
        print (f"BookArtistSets:get_queryset: author is '{self.author.name}'")
        queryset = CoverQuerys.set_covers_by_artist(author=self.author.author_id, return_dict=True)
        return queryset


class Edition(DetailView):
    model=Editions
    print ("Edition")
    template_name = 'bookcovers/edition.html'


#=========================================
# the simplest of generic class views simply provide the model
# this on its own lists all authors with context_object_name = author_list
#    model = Author

# To list a subset of the model object specify the list of objects 
# using queryset
# sort authors
#    queryset = Author.objects.order_by('name')
#    context_object_name = 'author_list'
#=========================================

