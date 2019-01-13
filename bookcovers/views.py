from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from django.db.models import F
from django.db.models import Q


from bookcovers.models import Authors
from bookcovers.models import Artists
from bookcovers.models import ArtistAkas
from bookcovers.models import Artworks
from bookcovers.models import Books
from bookcovers.models import Covers
from bookcovers.models import Editions

from bookcovers.cover_querys import CoverQuerys
from bookcovers.original_raw_querys import OriginalRawQuerys

from bookcovers.pagers import ArtistPager
from bookcovers.pagers import AuthorPager
from bookcovers.pagers import BookPager

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
    def title(self,value):
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


# ArtistList -> artist_book_covers -> books_per_artwork
# http:<host>/bookcovers/artists/
class ArtistList(SubjectList):
    template_name = 'bookcovers/artist_list.html'

    def __init__(self):
        self.title = "Artists"

    def get_queryset(self):
        print ("ArtistList: calling CoverQuerys.artist_list")
        #artist_list = Artists.objects.order_by('name')
        queryset = CoverQuerys.artist_list()
        return queryset

# http:<host>/bookcovers/artist/<artist_id>
# http:<host>/bookcovers/artist/<artist%20name>
# http:<host>/bookcovers/artist/<artist-slug>
def artist_book_covers(request, artist_id=None, name=None, slug=None):
    """
    displays thumbnails of books with covers by this artist
    :param request:
    one of
    :param artist_id:   ex: /bookcovers/artist/6/
    :param name:        ex: /bookcovers/artist/Jim%20Burns/
    :param slug:        ex: /bookcovers/artist/Jim-Burns/
    :return:
    """
    template_name = 'bookcovers/artist_book_covers.html'

    artist_pager = ArtistPager(request,  artist_id=artist_id, name=name, slug=slug)
    artist = artist_pager.get_entry()

    cover_list = CoverQuerys.artist_cover_list(artist=artist)
    print("cover_filepath is {}".format(artist.cover_filepath))
    context = {'artist': artist,
               'cover_list': cover_list,
               'subject_pager': artist_pager.get_subject_pager(),
               'meta_page':  artist_pager.meta_page()}
    return render(request, template_name, context)

# http:<host>/bookcovers/artist/<artwork_id>
def books_per_artwork(request, artwork_id):
    """
    displays all book covers using the same artwork, eg 'Dune' and 'The Three Stigmata of Palmer Eldritch' by BP
    or all book covers by same artist for the same title, eg two versions of "Decision at Doona" by BP
    :param request:
    :param artwork_id:  ex: /bookcovers/artwork_id/178/
    :return:
    """
    artwork = get_object_or_404(Artworks, artwork_id=artwork_id)

    # artist pager
    artist_pager = ArtistPager(request,  artist_id=artwork.artist_id)
    artist = artist_pager.get_entry()
    if artist_pager.get_request_page():
        # move on to the next or previous artist
        return redirect(to='bookcovers:artist_books', permanent=False, artist_id=artist.artist_id)

    # book cover pager
    page = request.GET.get('page')
    print(f"artwork cover_list: page is '{page}'")

    pager = BookPager(page=page, item_id=artwork_id)
    book_pager = pager.pager(book_cover_query=CoverQuerys.artist_cover_list,
                             item_id_key="artwork_id",
                             item_model=Artworks,
                             subject_id_key='artist_id',
                             subject_model=Artists)
    artwork = pager.get_entry()

    artwork_cover_list = CoverQuerys.all_covers_for_artwork(artwork)
    num_covers = len(artwork_cover_list)
    if num_covers == 1:
         # display the book detail
         edition = get_object_or_404(Editions, edition_id=artwork_cover_list[0]['edition__pk'])
    #     # maybe can have 1 template for book detail which can show multiples
    #     # rather than 3 templates with BookPager; books_per_artwork, covers_per_book, book_cover_detail
    #     # remember that when multiple covers we go down yet another level with cover pager as well
    #     # get subject pager working first to understand
    else:
        edition = None

    # display thumbnails of all covers for this artwork
    template_name = 'bookcovers/artist_books_per_artwork.html'
    context = {'artwork': artwork,
               'cover_list': artwork_cover_list,
               'subject_pager': artist_pager.get_subject_pager(),
               'meta_page': artist_pager.meta_page(),
               'book_pager': book_pager,
               'edition': edition}
    return render(request, template_name, context)


# AuthorList -> author_book_cover
# http:<host>/bookcovers/authors/
class AuthorList(SubjectList):
    template_name = 'bookcovers/author_list.html'

    def __init__(self):
        self.title = "Authors"

    def get_queryset(self):
        print ("AuthorList: calling CoverQuerys.author_list")
        queryset = CoverQuerys.author_list()
        return queryset

# http:<host>/bookcovers/author/<author_id>
# http:<host>/bookcovers/author/<author%20name>
# http:<host>/bookcovers/author/<author-slug>
def author_book_covers(request, author_id=None, name=None, slug=None):
    """
    displays thumbnails of books by this author
    :param request:
    one of
    :param author_id:   ex: /bookcovers/author/4/
    :param name:        ex: /bookcovers/artist/Robert%20Heinelein/
    :param slug:        ex: /bookcovers/author/Robert-Heinlein/
    :return:
    """
    template_name = 'bookcovers/author_book_covers.html'
    subject = "author"
    author_page = request.GET.get(subject)
    print(f"author_book_covers: author_page is '{author_page}'")

    author_pager = AuthorPager(request,  author_id=author_id, name=name, slug=slug)
    author = author_pager.get_entry()

    cover_list = CoverQuerys.all_covers_of_all_books_for_author(author=author, all=False)
    context = {'author': author,
               'cover_list': cover_list,
               'subject_pager': author_pager.get_subject_pager(),
               'meta_page':  author_pager.meta_page()}

    return render(request, template_name, context)

# http:<host>/bookcovers/book/<book_id>
def covers_per_book(request, book_id):
    """
    displays all the covers for the same book title
    :param request:
    :param book_id:     ex: /bookcovers/book/93/
    :return:
    """
    book = get_object_or_404(Books, pk=book_id)

    # author pager
    author_pager = AuthorPager(request, author_id=book.author_id)
    author = author_pager.get_entry()
    if author_pager.get_request_page():
        # move on to the next or previous author
        return redirect(to='bookcovers:author_books', permanent=False, author_id=author.author_id)

    # book cover pager
    page = request.GET.get('page')
    print(f"artwork cover_list: page is '{page}'")

    query_kwargs = {'author': book.author_id, 'all': False}
    pager = BookPager(page=page, item_id=book_id)
    book_pager = pager.pager(book_cover_query=CoverQuerys.books_for_author,
                             item_id_key="book_id",
                             item_model=Books,
                             subject_id_key='author_id',
                             subject_model=Authors)
    book = pager.get_entry()

    book_cover_list = CoverQuerys.all_covers_for_title(book)
    num_books = len(book_cover_list)
    if num_books == 1:
        # display the book detail
        edition = get_object_or_404(Editions, edition_id=book_cover_list[0]['edition__pk'])
    else:
        edition = None

    # display thumbnails of all covers for this book
    template_name = 'bookcovers/author_covers_per_book.html'
    #context = {'book': book, 'cover_list': book_cover_list}
    context = {'book': book,
               'cover_list': book_cover_list,
               'subject_pager': author_pager.get_subject_pager(),
               'meta_page': author_pager.meta_page(),
               'book_pager': book_pager,
               'edition': edition}
    return render(request, template_name, context)
    # return HttpResponse("Book Title: You're looking at book %s." % book.title)

def book_cover_detail(request, edition_id):
    # to consider: use this view for when go to edition without paging
    template_name = 'bookcovers/book_cover_detail.html'

    page = request.GET.get('page')
    print(f"book_cover_detail: page is '{page}'")

    # up to here
    # need subject pager here as well
    # need some kind of function for pagers
    # book pager and this view currently coded for artist book covers
    # ideally make generic for both artist book covers and author book covers
    # or need specific pager and views

    # edition -> cover -> artwork
    # TODO how to use get with filter rather than list?
    editions = Editions.objects \
        .filter(edition_id=edition_id) \
        .filter(theCover__flags__lt=256) \
        .values('edition_id',
                'theCover__artwork__pk',
                'book__title')
    artwork_id = editions[0]['theCover__artwork__pk']
    print (f"edition is {editions[0]['edition_id']}, artwork is {artwork_id}, book is '{editions[0]['book__title']}'")

    # up to here - currently trying to use this for both artists and author book detail
    # artwork = get_object_or_404(Artworks, artwork_id=artwork_id)
    # query_kwargs = {'artist': artwork.artist_id}
    # pager = BookPager(page=page, item_id=artwork_id)
    # book_pager = pager.pager(book_cover_query=CoverQuerys.artist_cover_list,
    #                          subject_id_key="artwork_id",
    #                          subject_model=Artworks)

    # if page:
    #     artwork = pager.get_entry()
    #     artwork_cover_list = CoverQuerys.all_covers_for_artwork(artwork)
    #     num_covers = len(artwork_cover_list)
    #     if num_covers > 1:
    #         return redirect('bookcovers:artwork', artwork_id=artwork.pk)
    #     else:
    #         edition_id = aßrtwork_cover_list[0]['edition__pk']

    edition = get_object_or_404(Editions, edition_id=edition_id)

    #context = {'edition': edition,  'book_pager': book_pager}
    context = {'edition': edition}
    return render(request, template_name, context)

class BookCoverDetail(DetailView):
    model=Editions
    template_name = 'bookcovers/book_cover_detail.html'


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

