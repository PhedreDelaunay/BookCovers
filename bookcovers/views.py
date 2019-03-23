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
        self._author = None

    def set_list(self):
        set_list = CoverQuerys.author_set_list(author_id=self.author.pk)
        return set_list

    def create_the_pager(self):
        author_pager = AuthorPager(self.request,  author_id=self.author_id, name=self.name, slug=self.slug)
        return author_pager

    def get_queryset(self):
        self.the_pager = self.create_the_pager()
        # get the author to display
        self.author = self.the_pager.get_entry()
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

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.artwork_id = kwargs.get("artwork_id", None)
        self.get_artwork(self.artwork_id)

    def get_object(self, queryset=None):
        # if multiple covers are returned exception will be caught and redirect to artwork list view
        cover = Covers.objects.get(artwork_id=self.artwork.pk, flags__lt=256)
        print (f"Artwork: get_object; cover is {cover}")
        edition = get_object_or_404(Editions, edition_id=cover.edition.pk)
        return edition

    def get(self, request, **kwargs):
        print (f"Artwork: get  - artist {self.artwork.artist_id}")
        self.the_pager = self.create_top_level_pager(self.artwork.artist_id)
        self.book_pager = self.create_book_pager()
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
        super().setup(request, *args, **kwargs)
        self.artwork_id = kwargs.get("artwork_id", None)
        self.get_artwork(self.artwork_id)

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(artist_id=self.artwork.artist_id)
        self.book_pager = self.create_book_pager()
        print (f"ArtworkList: get_queryset artwork.name={self.artwork.name}")
        queryset = CoverQuerys.all_covers_for_artwork(self.artwork)
        return queryset

# http:<host>/bookcovers/author/<author_id>/sets
# http:<host>/bookcovers/author/<author%20name>/sets
# http:<host>/bookcovers/author/<author-slug>/sets
def author_book_sets(request, author_id=None, name=None, slug=None):
    """
    displays thumbnails of books by this author ordered in sets by artist
    :param request:
    one of
    :param author_id:   ex: /bookcovers/author/15/sets
    :param name:        ex: /bookcovers/author/Ray%20Bradbury/sets
    :param slug:        ex: /bookcovers/author/Ray-Bradbury/sets
    :return:
    """
    template_name = 'bookcovers/author_book_sets.html'
    subject = "author"
    author_page = request.GET.get(subject)
    author_pager = AuthorPager(request,  author_id=author_id, name=name, slug=slug)
    author = author_pager.get_entry()
    print (f"author is {author}, {author.author_id}")

    # return_dict=True, return ValuesQuerySet, 1 query in 0.45MS
    # return_dict=False, return objects, 19 queries in 2.4MS
    cover_list = CoverQuerys.set_covers_by_artist(author=author.author_id, return_dict=True)
    num_covers = len(cover_list)
    #print (f"num_covers is {num_covers}")
    #print (f"cover_list is {cover_list}")

    context = {'author': author,
               'cover_list': cover_list,
               'the_pager': author_pager,}

    return render(request, template_name, context)
    #return HttpResponse("Book Sets: You're looking at sets for %s." % name)

# http:<host>/bookcovers/book/<book_id>
# http:<host>/bookcovers/book/<the%20title> - not implemented
class Book(AuthorMixin, DetailView):
    """
        display a single book title selected from an author's list
        redirect to BookList when multiple covers are returned
    """
    template_name = 'bookcovers/book.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.book_id = kwargs.get("book_id", None)
        # up to here do we really want to get book here. book pager gets actual book?
        self.get_book(book_id=self.book_id)

    def get_object(self, queryset=None):
        # if multiple covers are returned exception will be caught and redirect to artwork list view
        cover = Covers.objects.get(book=self.book_id, flags__lt=256)
        print (f"Book: get_object; cover is {cover}")
        edition = get_object_or_404(Editions, edition_id=cover.edition.pk)
        return edition

    def get(self, request, **kwargs):
        print (f"Book: get  - book {self.book_id}")
        self.the_pager = self.create_top_level_pager(author_id=self.book.author_id)
        self.book_pager = self.create_book_pager()
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
        self.get_book(book_id=self.book_id)

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(author_id=self.book.author_id)
        self.book_pager = self.create_book_pager()
        print (f"BookList: get_queryset book.title={self.book.title}")
        queryset = CoverQuerys.all_covers_for_title(self.book)
        return queryset

# up to here - errors if we remove this
# http:<host>/bookcovers/book/<book_id>
# http:<host>/bookcovers/book/<the%20title>
def book(request, book_id=None, title=None):
    """
    displays all the covers for the same book title
    :param request:
    :param book_id:     ex: /bookcovers/book/93/
    :param: title:      ex: /bookcovers/book/Machineries%20Of%20Joy/
                        not yet implemented
    :return:
    """
    author_id=None
    if book_id:
        book = get_object_or_404(Books, pk=book_id)
        author_id = book.author_id

    # author pager
    author_pager = AuthorPager(request, author_id=author_id)
    if author_pager.get_request_page():
        # move on to the next or previous author
        author = author_pager.get_entry()
        return redirect(to='bookcovers:author_books', permanent=False, author_id=author.author_id)

    # book cover pager
    page = request.GET.get('page')
    print(f"views:book: page is '{page}'")

    query_kwargs = {'author': book.author_id, 'all': False}
    pager = BookPager(page=page, item_id=book_id)
    book_pager = pager.pager(book_cover_query=CoverQuerys.books_for_author,
                             item_id_key="book_id",
                             item_model=Books,
                             subject_id_key='author_id',
                             subject_model=Author)
    book = pager.get_entry()

    book_cover_list = CoverQuerys.all_covers_for_title(book)
    num_books = len(book_cover_list)
    if num_books == 1:
        # display the book detail
        # the template includes template book_cover_detail.html
        edition = get_object_or_404(Editions, edition_id=book_cover_list[0]['edition__pk'])
    else:
        edition = None

    # display thumbnails of all covers for this book
    template_name = 'bookcovers/author_covers_per_book.html'
    context = {'book': book,
               'cover_list': book_cover_list,
               'the_pager': author_pager,
               'book_pager': book_pager,
               'edition': edition}
    return render(request, template_name, context)
    # return HttpResponse("Book Title: You're looking at book %s." % book.title)

def artwork_edition(request, edition_id):

    return book_edition(request, edition_id)

def book_edition(request, edition_id):
    author_id=None

    edition = Editions.objects.get(edition_id=edition_id,theCover__flags__lt=256)

    book = get_object_or_404(Books, pk=edition.book.pk)
    author_id = book.author_id

    # author pager
    author_pager = AuthorPager(request, author_id=author_id)
    if author_pager.get_request_page():
        # move on to the next or previous author
        author = author_pager.get_entry()
        return redirect(to='bookcovers:author_books', permanent=False, author_id=author.author_id)

    # book cover pager
    page = request.GET.get('page')
    print(f"artwork cover_list: page is '{page}'")

    query_kwargs = {'author': book.author_id, 'all': False}
    pager = BookPager(page=page, item_id=book.pk)
    book_pager = pager.pager(book_cover_query=CoverQuerys.books_for_author,
                             item_id_key="book_id",
                             item_model=Books,
                             subject_id_key='author_id',
                             subject_model=Author)
    book = pager.get_entry()

    # up to here need a cover pager

    context = {'book': book,
               'the_pager': author_pager,
               'book_pager': book_pager,
               'edition': edition}

    return book_cover_detail(request, edition_id, context)

def book_cover_detail(request, edition_id, context):
    # to consider: use this view for when go to edition without paging
    template_name = 'bookcovers/edition.html'

    page = request.GET.get('page')
    print(f"book_cover_detail: page is '{page}'")

    # edition -> cover -> artwork
    edition = Editions.objects.get(edition_id=edition_id,theCover__flags__lt=256)
    print (f"edition is {edition.pk}, artwork is {edition.theCover.artwork_id}, book is '{edition.book.title}'")

    return render(request, template_name, context)

class EditionDetail(DetailView):
    model=Editions
    print ("Edition detail")
    template_name = 'bookcovers/edition_detail.html'


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

