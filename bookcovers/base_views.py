# bookcovers/base_views.py

from django.views.generic import ListView



import math



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

    # setup is called when the class instance is created
    # note: not in 2.1, added in 2.2
    def setup(self, request, *args, **kwargs):
        print (request)
        super().setup(request, *args, **kwargs)
        self.screen_width = request.GET.get('screen_width')
        if not self.screen_width:
            self.screen_width = 0
        print(f"SubjectList::setup: screen_width='{ self.screen_width }'")
        if int(self.screen_width) > 0:
            num_cols = int(self.screen_width)/self.column_width
            self.num_columns = int(num_cols)
            print (f"num_cols is { num_cols }, num_columns is { self.num_columns }")
            result = float(self.screen_width)/self.column_width
            num_cols = int(result)
            decimal = result - num_cols
            if decimal > 0.98:
                num_cols += 1
            self.num_columns = num_cols
            print(
                f"result is { result }, num_cols is { num_cols }, decimal is { decimal }, num_columns is { self.num_columns }")



    # https://reinout.vanrees.org/weblog/2014/05/19/context.html
    # this is the old way of doing things as can reference view in template
    def get_context_data(self,**kwargs):
        context = super(SubjectList,self).get_context_data(**kwargs)
        context['title'] = self.title
        print ("title is '{0}'".format(self.title))
        column_length=self.get_num_rows(self.get_queryset(), self.num_columns)
        context['column_length'] = column_length
        context['screen_width'] = self.screen_width
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


