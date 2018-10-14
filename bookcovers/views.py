from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
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


def author_books(request, author_id=None, name=None, slug=None):
    template_name = 'bookcovers/cover_list.html'

    if author_id:
        kwargs = {'pk': author_id}
    elif name:
        kwargs = {'name': name}
    elif slug:
        slug = slug.replace('-', ' ')
        kwargs = {'name': slug}
    author = get_object_or_404(Authors, pk=author_id)
    return HttpResponse("You're looking at author %s." % author.name)

def artist_books(request, artist_id=None, name=None, slug=None):
    template_name = 'bookcovers/cover_list.html'

    if artist_id:
        kwargs = {'pk': artist_id}
    elif name:
        kwargs = {'name': name}
    elif slug:
        slug = slug.replace('-', ' ')
        kwargs = {'name': slug}

    artist = get_object_or_404(Artists, **kwargs)
    cover_list = CoverQuerys.artist_cover_list(artist)

    # render short cut
    #context = {'title': artist.name, 'cover_list': cover_list}
    # cover_list.object.html context = {'artist': artist, 'artwork_list': cover_list}
    print("cover_filepath is {}".format(artist.cover_filepath))
    context = {'artist': artist, 'cover_list': cover_list}

    return render(request, template_name, context)

def book_detail(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    return HttpResponse("You're looking at book %s." % book.title)

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

class AuthorList(SubjectList):
    template_name = 'bookcovers/author_list.html'

    def __init__(self):
        self.title = "Authors"

    def get_queryset(self):
        print ("AuthorList: calling CoverQuerys.author_list")
        queryset = CoverQuerys.author_list()
        return queryset

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





