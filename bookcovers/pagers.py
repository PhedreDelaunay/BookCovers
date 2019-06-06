from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


from bookcovers.models import Artist
from bookcovers.models import Author
from bookcovers.models import Panorama
from bookcovers.cover_querys import CoverQuerys

# just in case
# TODO read this
# http://blog.appliedinformaticsinc.com/how-to-build-custom-pagination-in-django-to-overcome-django-paginator-drawbacks/

class MenuPager():

    def __init__(self):
        # Show 1 cover work per page
        self.per_page = 1

    def get_entry(self):
        return self.entry

    def get_page_number(self):
        return self.page_number


class SubjectPager(MenuPager):
    """
    Pager for top level subject, ie artist, author,
    """
    def __init__(self, query_cache, page_number=None, subject_id=None, name=None, slug=None):
        """
        :param query_cache:
        :param page_number:     current page if set
        one of
        :param subject_id:      artist or author id
        :param name:            artist or author name
        :param slug:            artist or author slug
        """
        print(f"SubjectPager::init: subject_id={subject_id} name='{name}' slug='{slug}'")
        super(SubjectPager, self).__init__()
        self.query_cache = query_cache
        self.page_number = page_number
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
            self.subject_kwargs = {'pk': subject_id}
        elif name:
            self.subject_identifier = name
            self.subject_kwargs = {'name': name}
        elif slug:
            self.subject_identifier = slug
            self.subject_kwargs = {'slug': slug}

    def pager(self, cover_query, subject_id_key, subject_model):
        """
        :param cover_query:         query to get list of items to page
        :param subject_id_key:      key of id; artist_id, author_id
        :param subject_model:       model for item; Artists, Authors
        :return:
        """
        subject_list = cover_query()

        paginator = Paginator(object_list=subject_list, per_page=self.per_page)

        # have we got here by paging?
        if self.page_number:
            #print(f"subject_list[{self.page_number}-1] is {subject_list[int(self.page_number)-1]}")
            kwargs = {'pk': subject_list[int(self.page_number) - 1][subject_id_key]}
            self.entry = self.get_subject(**kwargs)
        else:
            self.entry = self.get_subject(**self.subject_kwargs)
            print(f"entry is {self.entry}")
            # Which page is the requested entry?
            print (f"SubjectPager: self.entry.pk is {self.entry.pk}")
            page_number = [count for count, record in enumerate(subject_list, 1) if record[subject_id_key] == self.entry.pk]
            self.page_number = int(page_number[0])
            print (f"SubjectPager figured out that page is {self.page_number}")

        print (f"SubjectPager: pager entry is '{self.entry}'")
        self.subject_pager = paginator.get_page(self.page_number)
        return self.subject_pager

    @property
    def subject_pager(self):
        return self._subject_pager

    @subject_pager.setter
    def subject_pager(self, value):
        self._subject_pager = value


class ArtistPager(SubjectPager):

    def __init__(self, request, query_cache, artist_id=None, name=None, slug=None):
        """
        :param request:
        :param query_cache:
        one of
        :param artist_id:      artist id
        :param name:           artist name
        :param slug:           artist slug
        """
        print(f"ArtistPager::init: artist_id={artist_id} name='{name}' slug='{slug}'")
        self.subject = 'artist'
        self.page_number = request.GET.get(self.subject)
        print(f"ArtistPager: page_number is '{self.page_number}'")
        super().__init__(query_cache, page_number=self.page_number, subject_id=artist_id, name=name, slug=slug)

        self.pager(cover_query=CoverQuerys.artist_list,
                   subject_id_key="artist_id",
                   subject_model=Artist)

    def get_subject(self, **kwargs):
        """
        subject is artist
        :param kwargs:
        :return:
        """
        artist = self.query_cache.artist(artist=None, **kwargs)
        return artist


class AuthorPager(SubjectPager):

    def __init__(self, request, query_cache, author_id=None, name=None, slug=None):
        """
        :param request:
        :param query_cache:
        one of
        :param author_id:      author id
        :param name:           author name
        :param slug:           author slug
        """
        self.subject = 'author'
        self.page_number = request.GET.get(self.subject)
        print(f"AuthorPager: page_number is '{self.page_number}'")
        super().__init__(query_cache, page_number=self.page_number, subject_id=author_id, name=name, slug=slug)

        self.pager(cover_query=CoverQuerys.author_list,
                   subject_id_key="author_id",
                   subject_model=Author)

    def get_subject(self, **kwargs):
        """
        subject is author
        :param kwargs:
        :return:
        """
        author = self.query_cache.author(author=None, **kwargs)
        return author


class PanoramaPager(SubjectPager):

    def __init__(self, request, query_cache, panorama_id=None, name=None, slug=None):
        """
        :param request:
        :param query_cache:
        one of
        :param panorama_id:    panorama id
        :param name:           panorama name  - not implemented
        :param slug:           panorama slug - not implemented
        """
        print(f"PanoramaPager::init: panorama_id={panorama_id} name='{name}' slug='{slug}'")
        self.subject = 'panorama'
        self.page_number = request.GET.get(self.subject)
        print(f"PanoramaPager: page_number is '{self.page_number}'")
        super().__init__(query_cache, page_number=self.page_number, subject_id=panorama_id, name=name, slug=slug)

        self.pager(cover_query=CoverQuerys.panorama_list,
                   subject_id_key="panorama_id",
                   subject_model=Panorama)

    def get_subject(self, **kwargs):
        """
        subject is panorama
        :param kwargs:
        :return:
        """
        panorama = self.query_cache.panorama(**kwargs)
        #panorama = get_object_or_404(Panorama, **kwargs)
        print(f"panorama is {panorama}")
        return panorama

    # todo move these to base class
    def get_page_number(self):
        return self.page_number


class SecondLevelPager(MenuPager):
    """
    Pager for second level items
    ie book covers for artwork (from artist) or book covers for book title (from author)
    """
    def __init__(self, query_cache, page_number=None, item_id=None):
        """
        :param query_cache:
        :param page_number:  current page if set
        :param item_id:      artwork or book id
        """
        super().__init__()
        self.query_cache = query_cache
        self.page_number = page_number
        self.item_id = item_id

    def pager(self, book_cover_query, item_id_key):
        """
        :param book_cover_query:    query to get list of book covers to page
        :param item_id_key:         string key of item id; artwork_id, book_id
        :return:
        """
        # item is artwork or book
        item = self.get_item(self.item_id)
        list = self.get_list(item, book_cover_query)

        print (f"SecondLevelPager page_number is {self.page_number}")
        # have we got here by paging?
        if self.page_number:
            item_id = list[int(self.page_number) - 1][item_id_key]
            print(f"SecondLevelPager::pager now item_id is '{item_id}'")
            self.entry = self.get_item(item_id)
        else:
            self.entry = item

        # Show 1 book title per page
        paginator = Paginator(list, 1)

        if not self.page_number:
            # Which page is the requested entry?
            page_number = [count for count, record in enumerate(list, 1) if record[item_id_key] == item.pk]
            self.page_number = int(page_number[0])
            print (f"BookPager figured out that page_number is {self.page_number}")

        second_level_pager = paginator.get_page(self.page_number)
        return second_level_pager

    def get_list(self, item, list_query):
        book_cover_list = list_query(item.get_creator)
        print (f"SecondLevelPager::pager: book_cover_list is '{book_cover_list}'")
        return book_cover_list


class BookPager(SecondLevelPager):
    """
    Pager for second level book list,
    ie book covers for artwork (from artist) or book covers for book title (from author)
    """
    def get_item(self, book_id):
        # item is book
        book = self.query_cache.book(book_id=book_id)
        print(f"BookPager::get_item: book_id = '{book_id}'")
        return book


class ArtworkPager(BookPager):
    def get_item(self, artwork_id):
        # item is artwork
        artwork = self.query_cache.artwork(artwork_id=artwork_id)
        print(f"ArtworkPager::get_item: artwork_id = '{artwork_id}'")
        return artwork

# up to here - refactor to use get_item make second level page and derive BookPager, ArtworkPager, SetPager
# with get_item, get_list and other methods called from pager method
class SetPager(SecondLevelPager):
    """
    Pager for second level set list,
    ie book covers for artwork (from artist) or book covers for book title (from author)
    """
    def get_item(self, set_id):
        # item is a set
        item = self.query_cache.set(set_id=set_id)
        print(f"SetPager::get_item: set_id = '{set_id}'")
        return item

    # need to know if author or artist
    # BookPager originally took subject_model as parameter, maybe add it to init
    # def get_list(self, item, list_query):
    #     creators = item.get_creator
    #     print (f"SetPager::pager creators is '{creators.author}, {creators.artist}'")
    #     creator=subject_model._meta.model_name
    #     set_list = set_query(getattr(creators, creator).pk)
    #     return book_cover_list


    def pager(self, set_query, item_id_key, item_model, subject_model):
        """
        :param set_query:    query to get list of sets to page
        :param item_id_key:         string key of item id; set_id
        :param item_model:          model for item; Sets
        :param subject_model:       model for subject; Artists, Authors
        :return:
        """

        # item is set
        item = self.get_item(self.item_id)

        creators = item.get_creator
        print (f"SetPager::pager creators is '{creators.author}, {creators.artist}'")
        creator=subject_model._meta.model_name
        set_list = set_query(getattr(creators, creator).pk)
        #print (f"SetPager::pager set_list is'{set_list}'")

        print (f"SetPager page_number is {self.page_number}")
        # have we got here by paging?
        if self.page_number:
            # print(f"set_list[{self.page_number}-1] is {set_list[int(self.page_number)-1]}")
            # kwargs = {'pk': set_list[int(self.page_number) - 1][item_id_key]}
            # self.entry = get_object_or_404(item_model, **kwargs)
            item_id = set_list[int(self.page_number) - 1][item_id_key]
            print(f"SetPager::pager now item_id is '{item_id}'")
            self.entry = self.get_item(item_id)
        else:
            self.entry = item

        # /Users/tarbetn/Projects/BookCovers/bookcovers/pagers.py:262: UnorderedObjectListWarning:
        # Pagination may yield inconsistent results with an unordered object_list: <class 'bookcovers.models.Set'> QuerySet.
        #   paginator = Paginator(set_list, 1)
        # Show 1 set per page
        paginator = Paginator(set_list, 1)

        if not self.page_number:
            # Which page is the requested entry?
            page_number = [count for count, record in enumerate(set_list, 1) if record[item_id_key] == item.pk]
            self.page_number = int(page_number[0])
            print (f"SetPager figured out that page_number is {self.page_number}")

        set_pager = paginator.get_page(self.page_number)
        return set_pager