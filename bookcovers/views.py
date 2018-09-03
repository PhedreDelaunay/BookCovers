from django.shortcuts import get_object_or_404, render
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
    return HttpResponse("Hello Django World")

def author_books(request, author_id):
    author = get_object_or_404(Authors, pk=author_id)
    return HttpResponse("You're looking at author %s." % author.name)

def artist_books(request, artist_id):
    template_name = 'bookcovers/cover_list.html'

    artist = get_object_or_404(Artists, pk=artist_id)

    OriginalRawQuerys.artist_cover_list(artist_id)
    cover_list = CoverQuerys.artist_cover_list(artist_id)

    # render short cut
    context = {'title': artist.name, 'cover_list': cover_list}
    return render(request, template_name, context)

def book_detail(request, book_id):
    book = get_object_or_404(Books, pk=book_id)
    return HttpResponse("You're looking at book %s." % book.title)

# https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/
class SubjectList(ListView):
    num_columns=6
    template_name = 'bookcovers/subject_list.html'

    # https://docs.djangoproject.com/en/2.0/topics/class-based-views/generic-display/#making-friendly-template-contexts
    # in template object_list is called item_list
    context_object_name = 'item_list'

    def get_context_data(self,**kwargs):
        print ("entering get_context_data")
        context = super(SubjectList,self).get_context_data(**kwargs)
        context['title'] = self.title
        print ("title is '{0}'".format(self.title))
        column_length=self.get_num_rows(self.queryset, self.num_columns)
        context['column_length'] = column_length
        return context

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,value):
        self._title = value

    def get_num_rows(self, queryset, num_columns):
        # round up
        num_rows = math.ceil(queryset.count()/num_columns)
        print ("num_rows is {0}".format(num_rows))
        return num_rows


class ArtistList(SubjectList):
    template_name = 'bookcovers/artist_list.html'

    def __init__(self):
        self.title = "Artists"

    artist_list = Artists.objects.order_by('name')
    queryset = artist_list

class AuthorList(SubjectList):
    def __init__(self):
        self.title = "Authors"

    template_name = 'bookcovers/author_list.html'

# this on its own lists all authors with context_object_name = author_list
#    model = Author

    # sort authors
#    queryset = Author.objects.order_by('name')
#    context_object_name = 'author_list'
#=========================================

    #OriginalRawQuerys.author_list()
    queryset = CoverQuerys.author_list()




