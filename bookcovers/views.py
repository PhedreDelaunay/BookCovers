
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView

from bookcovers.models import Edition
from bookcovers.models import Panorama
from bookcovers.cover_querys import CoverQuerys
from bookcovers.pagers import PanoramaPager

import math

# Create your views here.

def index(request):
    print ("index: hello page")
    return HttpResponse("Hello Django World")


class PrintHistory(ListView):
    """
        displays print runs
    """
    template_name = 'bookcovers/print_history.html'
    context_object_name = 'print_history'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.print_run_id = kwargs.get("print_run_id", None)

    def get_queryset(self):
        queryset = CoverQuerys.print_history(self.print_run_id)
        return queryset

class Edition(DetailView):
    model=Edition
    context_object_name="edition"
    print ("Edition")
    template_name = 'bookcovers/edition.html'

class PanoramaList(ListView):
    model=Panorama
    context_object_name="panorama_list"
    web_title = "Panoramas"
    print ("Panoramas")
    template_name = 'bookcovers/panoramas.html'

    def get_queryset(self):
        queryset = CoverQuerys.panorama_list()
        return queryset


class Panorama(DetailView):
    model=Panorama
    context_object_name="panorama"
    print ("Panorama")
    template_name = 'bookcovers/panorama.html'

    subject_list = {
        'title': 'panoramas',
        'view_name': 'panoramas',
        'object': None,
    }

    subject = {
        'name': 'panorama',
        'title': 'panoramas',
        'view_name': 'panorama',
        'set_view_name': None,
        'object': None,
    }
    def get_object(self, queryset=None):
        panorama_id = self.kwargs.get("pk")
        panorama = CoverQuerys.panorama(pk=panorama_id)
        print (f"Panorama::get_object: panorama is '{panorama_id}'")
        query_cache = None
        self.the_pager = PanoramaPager(self.request, query_cache, panorama_id=panorama_id)
        panorama = self.the_pager.get_entry()
        return panorama

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

