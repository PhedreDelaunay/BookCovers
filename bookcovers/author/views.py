from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic import DetailView

from bookcovers.models import Edition
from bookcovers.cover_querys import CoverQuerys
from bookcovers.views import SubjectList

from .view_mixin import AuthorMixin

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
        #self._author = None
        print (f"AuthorBooks::setup: author_id='{self.author_id}', name='{self.name}', slug='{self.slug}'")

    def set_list(self):
        set_list = CoverQuerys.author_set_list(author_id=self.author.pk)
        return set_list

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(author_id=self.author_id, name=self.name, slug=self.slug)
        self.author = self.the_pager.get_entry()
        print (f"AuthorBooks:get_queryset: author is '{self.author.name}'")
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

# http:<host>/bookcovers/book/<book_id>
# http:<host>/bookcovers/book/<the%20title> - not implemented
class Book(AuthorMixin, DetailView):
    template_name = 'bookcovers/book.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.book_id = kwargs.get("book_id", None)
        self.detail['list_view_name'] = 'books'
        # why does AuthorMixin not reset between views?
        # cos it is class variable not instance variable

    def get_object(self, queryset=None):
        self.create_pagers(book_id=self.book_id)
        self.cover_list = CoverQuerys.all_covers_for_title(self.book)
        edition = get_object_or_404(Edition, edition_id=self.cover_list[0]['edition_id'])
        return edition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print ("Book: get_context")
        context['cover_list'] = self.cover_list
        return context


# http:<host>/bookcovers/book/edition/<edition_id>
class BookEdition(Book):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        self.detail['view_name'] = 'book_edition'

    def get_object(self, queryset=None):
        edition = get_object_or_404(Edition, edition_id=self.edition_id)
        self.create_pagers(book_id=edition.book.pk)
        self.cover_list = CoverQuerys.all_covers_for_title(self.book)
        return edition

# http:<host>/bookcovers/books/<book_id>
class Books(AuthorMixin, ListView):
    """
        displays all the book covers for the same book title
    """
    template_name = 'bookcovers/books.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.book_id = kwargs.get("book_id", None)

    def get_queryset(self):
        self.create_pagers(book_id=self.book_id)
        print (f"Books: get_queryset book.title={self.book.title}")
        queryset = CoverQuerys.all_covers_for_title(self.book)
        return queryset

# http:<host>/bookcovers/author/<author%20name>/sets
class AuthorSets(AuthorMixin, ListView):
    """
    displays thumbnails of books by this author ordered in sets by artist
    """
    template_name = 'bookcovers/author_sets.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.name = kwargs.get("name", None)
        print (f"AuthorSets::setup: author={self.name}")

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(name=self.name)
        self.author = self.the_pager.get_entry()
        self.web_title = self.author.name
        print (f"AuthorSets:get_queryset: author is '{self.author.name}'")
        queryset = CoverQuerys.author_set_covers(author_id=self.author.author_id, return_dict=True)
        return queryset

# http:<host>/bookcovers/book/set/edition/<edition_id>
class SetEdition(Book):
    template_name = 'bookcovers/set_edition.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        self.detail['list_view_name'] = 'set_editions'
        self.detail['view_name'] = 'set_edition'
        self.detail['to_page_view_name'] = 'book_set_detail'

    def get_object(self, queryset=None):
        edition = get_object_or_404(Edition, edition_id=self.edition_id)
        print (f"SetEdition:get_object author id is '{edition.book.author_id}'")
        print (f"SetEdition:get_object artist id is '{edition.theCover.artwork.artist_id}'")
        set, self.cover_list = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)
        self.set_pager = self.create_set_pager(set_id=set.pk)
        self.the_pager = self.create_top_level_pager(author_id=edition.book.author_id)
        self.detail['object'] = edition
        self.author = edition.book.author
        self.web_title = edition.book.author.name
        return edition

# http:<host>/bookcovers/book/set/detail/<set_id>
class BookSetDetail(SetEdition):
    """
        displays detail for the edition and thumbnails for the associated editions in the set given the set id
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.set_id = kwargs.get("set_id", None)
        print (f"BookSetDetail::setup set_id is '{self.set_id}'")

    def get_object(self, queryset=None):
        self.set_pager = self.create_set_pager(set_id=self.set_id)
        # TODO create_set_pager sets self.set but this is not obvious, make more explicit
        set, self.cover_list = CoverQuerys.author_artist_set_cover_list(set_id=self.set.pk)
        edition = get_object_or_404(Edition, edition_id=self.cover_list[0]['edition_id'])
        self.the_pager = self.create_top_level_pager(author_id=edition.book.author_id)
        self.detail['object'] = edition
        self.web_title = edition.theCover.book.author.name
        return edition

# http:<host>/bookcovers/book/set/editions/<edition_id>
class SetEditions(AuthorMixin, ListView):
    """
        displays all the covers for the set
    """
    template_name = 'bookcovers/set_editions.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        print (f"SetEditions::setup: edition_id is {self.edition_id}")
        self.detail['view_name'] = 'set_edition'
        self.detail['to_page_view_name'] = 'book_set_list'

    def get_queryset(self):
        edition = get_object_or_404(Edition, edition_id=self.edition_id)
        print (f"SetEditions:get_object author id is '{edition.book.author_id}'")
        print (f"SetEditions:get_object artist id is '{edition.theCover.artwork.artist_id}'")
        self.create_pagers(book_id=edition.book.pk)
        set, queryset = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)

        self.book = edition.book
        self.set_pager = self.create_set_pager(set_id=set.pk)
        return queryset


# http:<host>/bookcovers/book/set/list/<set_id>
class BookSetList(SetEditions):
    """
        displays all the covers for the set given the set id
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.set_id = kwargs.get("set_id", None)
        print (f"ArtworkSetList::setup set_id is '{self.set_id}'")

    def get_queryset(self):
        self.set_pager = self.create_set_pager(set_id=self.set_id)
        # TODO create_set_pager sets self.set but this is not obvious, make more explicit
        set, queryset = CoverQuerys.author_artist_set_cover_list(set_id=self.set.pk)
        edition = get_object_or_404(Edition, edition_id=queryset[0]['edition_id'])
        self.the_pager = self.create_top_level_pager(author_id=edition.book.author_id)
        self.detail['object'] = edition
        self.author = edition.book.author
        self.web_title = self.author.name
        return queryset