
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView

from bookcovers.models import Edition
from bookcovers.cover_querys import CoverQuerys

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
    # this no longer works due to use of views in detail.html
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

