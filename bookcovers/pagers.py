from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from django.apps import apps

from bookcovers.models import Artists
from bookcovers.models import Artworks
from bookcovers.models import Author
from bookcovers.cover_querys import CoverQuerys
from bookcovers.record_helper import *

class MenuPager():

    def __init__(self):
        # Show 1 cover work per page
        self.per_page = 1

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self,value):
        self._subject = value

    @property
    def subject_title(self):
        return self._subject_title

    @subject_title.setter
    def subject_title(self,value):
        self._subject_title = value



class SubjectPager(MenuPager):
    """
    Pager for top level subject, ie artist, author,
    """
    def __init__(self, page=None, subject_id=None, name=None, slug=None):
        """
        :param page:            current page if set
        one of
        :param subject_id:      artist or author id
        :param name:            artist or author name
        :param slug:            artist or author slug
        """
        super(SubjectPager, self).__init__()
        self.page = page
        self.subject_id = subject_id
        self.name = name
        self.slug = slug
        self.set_subject_identifier(subject_id=subject_id, name=name, slug=slug)

    @property
    def subject_identifier(self):
        return self._subject_identifier

    @subject_identifier.setter
    def subject_identifier(self, value):
        self._subject_identifier = value

    def set_subject_identifier(self, subject_id=None, name=None, slug=None):
        if subject_id:
            self.subject_identifier = subject_id
        elif name:
            self.subject_identifier = name
        elif slug:
            self.subject_identifier = slug

    def pager(self, cover_query, subject_id_key, subject_model):
        """
        :param cover_query:         query to get list of items to page
        :param subject_id_key:      key of id; artist_id, author_id
        :param subject_model:       model for item; Artists, Authors
        :return:
        """
        # TODO can queries be cached between pages?
        subject_list = cover_query()

        paginator = Paginator(object_list=subject_list, per_page=self.per_page)

        # have we got here by paging?
        if self.page:
            print(f"subject_list[{self.page}-1] is {subject_list[int(self.page)-1]}")
            kwargs = {'pk': subject_list[int(self.page) - 1][subject_id_key]}
            self.entry = get_object_or_404(subject_model, **kwargs)
        else:
            self.entry = get_subject_record(model=subject_model, subject_id=self.subject_id, name=self.name, slug=self.slug)

        print (f"SubjectPager: pager entry is '{self.entry}'")
        if not self.page:
            # Which page is the requested entry?
            page = [count for count, record in enumerate(subject_list, 1) if record[subject_id_key] == self.entry.pk]
            self.page = int(page[0])
            print (f"SubjectPager figured out that page is {self.page}")

        self.subject_pager = paginator.get_page(self.page)
        return self.subject_pager

    def get_entry(self):
        return self.entry

    @property
    def subject_pager(self):
        return self._subject_pager

    @subject_pager.setter
    def subject_pager(self, value):
        self._subject_pager = value


class ArtistPager(SubjectPager):

    def __init__(self, request, artist_id=None, name=None, slug=None):
        """
        :param request:
        one of
        :param artist_id:      artist id
        :param name:           artist name
        :param slug:           artist slug
        """
        self.subject = 'artist'
        self.request_page = request.GET.get(self.subject)
        print(f"ArtistPager: request_page is '{self.request_page}'")
        super(ArtistPager, self).__init__(page=self.request_page, subject_id=artist_id, name=name, slug=slug)

        self.subject_title = "Artist"

        self.pager(cover_query=CoverQuerys.artist_list,
                               subject_id_key="artist_id",
                               subject_model=Artists)

    def get_request_page(self):
        return self.request_page

class AuthorPager(SubjectPager):

    def __init__(self, request, author_id=None, name=None, slug=None):
        """
        :param request:
        one of
        :param author_id:      author id
        :param name:           author name
        :param slug:           author slug
        """
        self.subject = 'author'
        self.request_page = request.GET.get(self.subject)
        print(f"AuthorPager: request_page is '{self.request_page}'")
        super(AuthorPager, self).__init__(page=self.request_page, subject_id=author_id, name=name, slug=slug)

        self.subject_title = "Author"

        self.pager(cover_query=CoverQuerys.author_list,
                   subject_id_key="author_id",
                   subject_model=Author)

    def get_request_page(self):
        return self.request_page

class BookPager(MenuPager):
    """
    Pager for second level book list,
    ie book covers for artwork (from artist) or book covers for book title (from author)
    """
    def __init__(self, page=None, item_id=None):
        """
        :param page:            current page if set
        one of
        :param item_id:      artwork or book id
        """
        super(MenuPager, self).__init__()
        self.page = page
        self.item_id = item_id

    def pager(self, book_cover_query, item_id_key, item_model, subject_id_key, subject_model):
        """
        :param book_cover_query:    query to get list of book covers to page
        :param item_id_key:         string key of item id; artwork_id, book_id
        :param item_model:          model for item; Artworks, Books
        :param subject_id_key:      string key of subject id; artist_id, subject_id
        :param subject_model:       model for subject; Artists, Authors
        :return:
        """
        # have we got here by paging?
        if not self.page:
            if self.item_id:
                kwargs = {'pk': self.item_id}
                #self.entry = get_object_or_404(subject_model, **kwargs)
                print (f"self.item_id is '{self.item_id}'")

        # item is artwork or book
        kwargs = {item_id_key: self.item_id}
        item = get_object_or_404(item_model, **kwargs)
        kwargs = {subject_id_key: item.get_creator().pk}
        for key, value in kwargs.items():
            print (f"key '{key}': '{value}'")

        subject = get_object_or_404(subject_model, **kwargs)
        book_cover_list = book_cover_query(subject)

        print (f"BookPager page is {self.page}")
        if self.page:
            print(f"book_cover_list[{self.page}-1] is {book_cover_list[int(self.page)-1]}")
            kwargs = {'pk': book_cover_list[int(self.page) - 1][item_id_key]}
            self.entry = get_object_or_404(item_model, **kwargs)
        else:
            self.entry = item

        # Show 1 book title per page
        paginator = Paginator(book_cover_list, 1)

        if not self.page:
            # Which page is the requested entry?
            page = [count for count, record in enumerate(book_cover_list, 1) if record[item_id_key] == item.pk]
            self.page = int(page[0])
            print (f"BookPager figured out that page is {self.page}")

        book_pager = paginator.get_page(self.page)
        return book_pager

    def get_entry(self):
        return self.entry