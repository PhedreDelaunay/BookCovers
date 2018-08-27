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

    aka_inner_queryset = Artists.objects.filter(artist_aka__artist_aka_id=artist_id)
    #print (aka_inner_queryset.query)
    #print (aka_inner_queryset)

    cover_list = Artworks.objects. \
        filter(Q(artist=artist_id) | Q(artist__in=aka_inner_queryset)). \
        filter(cover__flags__lt=256).values('book','book__title','artist__cover_filepath','cover__cover_filename')
# <a href="BookCoverDetail.php?filter=1&amp;ID=2&amp;bookID=82&amp;currentBook=14&amp;totalBooks=64&amp;currentEntry=12&amp;totalEntrys=115">
# <IMG src="http://www.djabbic.co.uk/BookCovers/Images/BrucePennington/Thumbnails/DecisionAtDoona_1971.jpg" class="special" alt="book title"></a>
    print (cover_list.query)
    print (cover_list)

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

    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/
    # If you only pass in a single field, you can also pass in the flat parameter. 
    # If True, this will mean the returned results are single values, rather than one-tuples.

    # djabbic v1
    #inner_queryset = BookEdition.objects.filter(book_edition_id=F('bookcover__book_edition_id')).filter(bookcover__flags__lt=256).values_list('book_edition_id',flat=True)
    # https://docs.djangoproject.com/en/2.0/topics/db/queries/#backwards-related-objects

    # djabbic_v2
    inner_queryset = Editions.objects. \
        filter(edition_id=F('covers__edition')). \
        filter(covers__flags__lt=256). \
        values_list('edition_id',flat=True)
    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/
    # flat=True returns a list of single items for a single field

    print (inner_queryset.query)
    print (inner_queryset.count())
    print (inner_queryset)

    # djabbic_v2
    # related_name vs related_query_name
    # why is above covers and gives error for cover
    # django.core.exceptions.FieldError: Cannot resolve keyword 'cover' into field. 
    # Choices are: book, book_id, catalog_number, country_id, covers, currency_id, designer, edition_id, flags, 
    # format_id, genre_id, imprint_id, isbn, isbn13, notes, print_run_id, print_year, purchase_price, purchase_year
    # yet below is book and gives error for books
    # django.core.exceptions.FieldError: Cannot resolve keyword 'books' into field. 
    # Choices are: author_id, birthplace, book, date_of_birth, date_of_death, flags, fullname, name, nationality, notes, website

    # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#in
    # need to clean database

    # djabbic v1
    # author_list = Author.objects.filter(author_id=F('book__author_id')).filter(book__book_id=F('book__edition__book_id')).filter(book__edition__book_edition_id__in=inner_queryset).values('name').order_by('name').distinct()

    # djabbic_v2
    author_list = Authors.objects. \
        filter(author_id=F('book__author')). \
        filter(book__book_id=F('book__edition__book')). \
        filter(book__edition__edition_id__in=inner_queryset). \
        values('author_id','name'). \
        order_by('name'). \
        distinct()

    print (author_list.query)
    print (author_list.count())
    queryset = author_list




