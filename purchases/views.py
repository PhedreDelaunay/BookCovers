from django.shortcuts import render
from django.views.generic import ListView
from django.db.models.functions import Lower

from purchases.models import Owned

# Create your views here.

class OwnedList(ListView):

    model = Owned
    template_name = 'purchases/owned.html'
    context_object_name = 'books'  # template context
    paginate_by = 500  # if pagination is desired

    queryset = Owned.objects.order_by(Lower('author_name'))
    print (f"number of owned items {len(queryset)}")

class OwnedAlphaList(ListView):
    """
        displays list of books for authors beginning with this letter
    """
    template_name = 'purchases/owned.html'
    context_object_name = 'books'      # template context
    #paginate_by = 200  # if pagination is desired

    def get_queryset(self):
        queryset = Owned.objects.filter(author_name__istartswith=self.kwargs["letter"]).order_by(Lower('author_name'))
        return queryset

