from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.core.paginator import Paginator
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

import math

# Create your views here.

def index(request):
    print ("index: hello page")
    return HttpResponse("Hello Django World")

def transform_slug(slug):
    slug = slug.replace('__', '%')
    slug = slug.replace('-', ' ')
    slug = slug.replace('%', '-')

    return slug

# https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/
class SubjectList(ListView):
    num_columns=6
    template_name = 'bookcovers/subject_list.html'

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


class ArtistList(SubjectList):
    template_name = 'bookcovers/artist_list.html'

    def __init__(self):
        self.title = "Artists"

    def get_queryset(self):
        print ("ArtistList: calling CoverQuerys.artist_list")
        #artist_list = Artists.objects.order_by('name')
        queryset = CoverQuerys.artist_list()
        return queryset


def artist_books(request, artist_id=None, name=None, slug=None):
    """
    displays thumbnails of books with covers by this artist
    :param request:
    :param artist_id:   ex: /bookcovers/artist/6/
    :param name:        ex: /bookcovers/artist/Jim%20Burns/
    :param slug:        ex: /bookcovers/artist/Jim-Burns/
    :return:
    """
    template_name = 'bookcovers/artist_cover_list.html'

    # pagination for artist second level menu
    # TODO can queries be cached between pages?
    artist_list = CoverQuerys.artist_list()

    # have we got here by paging?
    page = request.GET.get('page')

    # Show 1 artist's work per page
    paginator = Paginator(artist_list, 1)

    print (f"page is {page}")
    if page:
        print (f"artist_list[{page}-1] is {artist_list[int(page)-1]}")
        artist_id = artist_list[int(page)-1]['artist_id']

    if artist_id:
        kwargs = {'pk': artist_id}
    elif name:
        kwargs = {'name': name}
    elif slug:
        slug = transform_slug(slug)
        kwargs = {'name': slug}

    artist = get_object_or_404(Artists, **kwargs)
    if not page:
        # Which page is the requested artist?
        page = [count for count, record in enumerate(artist_list, 1) if record['artist_id'] == artist.artist_id]
        page = int(page[0])
        print (f"figured out that page is {page}")

    artist_page = paginator.get_page(page)

    cover_list = CoverQuerys.artist_cover_list(artist)
    print("cover_filepath is {}".format(artist.cover_filepath))
    context = {'artist': artist, 'cover_list': cover_list, 'artist_page': artist_page}
    return render(request, template_name, context)

def artwork_cover_list(request, artwork_id):
    """
    displays all covers using the same artwork
    or all covers by same artist for the same title
    :param request:
    :param artwork_id:
    :return:
    """
    artwork = get_object_or_404(Artworks, artwork_id=artwork_id)
    artwork_cover_list = CoverQuerys.all_covers_for_artwork(artwork)
    num_covers = len(artwork_cover_list)
    if num_covers == 1:
        # display the book detail
        return redirect('bookcovers:edition', pk=artwork_cover_list[0]['edition__pk'])

    # display thumbnails of all covers for this artwork
    template_name = 'bookcovers/book_cover_list.html'
    context = {'cover_list': artwork_cover_list}
    return render(request, template_name, context)

class AuthorList(SubjectList):
    template_name = 'bookcovers/author_list.html'

    def __init__(self):
        self.title = "Authors"

    def get_queryset(self):
        print ("AuthorList: calling CoverQuerys.author_list")
        queryset = CoverQuerys.author_list()
        return queryset

def author_books(request, author_id=None, name=None, slug=None):
    """
    displays thumbnails of books by this author
    :param request:
    :param author_id:   ex: /bookcovers/author/4/
    :param name:        ex: /bookcovers/artist/Robert%20Heinelein/
    :param slug:        ex: /bookcovers/author/Robert-Heinlein/
    :return:
    """
    template_name = 'bookcovers/author_book_list.html'

    if author_id:
        kwargs = {'pk': author_id}
    elif name:
        kwargs = {'name': name}
    elif slug:
        slug = transform_slug(slug)
        kwargs = {'name': slug}
    author = get_object_or_404(Authors, **kwargs)
    cover_list = CoverQuerys.all_covers_of_all_books_for_author(author=author, all=False)

    #return HttpResponse("You're looking at author %s." % author.name)
    context = {'author': author, 'cover_list': cover_list}
    return render(request, template_name, context)

def book_cover_list(request, book_id):
    """
    displays all the covers for the same title
    :param request:
    :param book_id:
    :return:
    """
    book = get_object_or_404(Books, pk=book_id)
    return HttpResponse("Book Title: You're looking at book %s." % book.title)


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





