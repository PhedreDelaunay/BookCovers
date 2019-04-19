from django.shortcuts import get_object_or_404

from bookcovers.pagers import AuthorPager
from bookcovers.pagers import ArtistPager
from bookcovers.pagers import BookPager

from bookcovers.cover_querys import CoverQuerys
from bookcovers.models import Author
from bookcovers.models import Books

from bookcovers.view_mixin import TopLevelPagerMixin


class AuthorMixin(TopLevelPagerMixin):
    subject_list = {
        'title': 'authors',
        'view_name': 'authors',
        'object': None,
    }
    subject = {
        'name': 'author',
        'title': 'books',
        'view_name': 'author_books',
        'set_view_name': 'author_sets',
        'object': None,
    }
    detail = {
        'to_page_view_name': 'book',
        'view_name': 'book_edition',
        'list_view_name': 'books',
        'object': None,
    }

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        print (f"author_setter: value is {value}")
        self._author = value
        self.subject['object'] = self._author

    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, value):
        print(f"book_setter: value is {value}")
        self._book = value
        self.set_book_attributes(self._book)

    def set_book_attributes(self, book):
        self.detail['object'] = book
        self.author = book.author
        self.book_id = book.pk
        self.web_title = book.title
        self.author_id = book.author_id

    def create_top_level_pager(self, author_id=None, name=None, slug=None):
        author_pager = AuthorPager(self.request, author_id=author_id, name=name, slug=slug)
        return author_pager

    def create_book_pager(self, book_id):
        # book title pager
        page_number = self.request.GET.get('page')
        print(f"AuthorMixin: create_book_pager - page_number is '{page_number}'")

        pager = BookPager(page_number=page_number, item_id=book_id)
        book_pager = pager.pager(book_cover_query=CoverQuerys.books_for_author,
                                 item_id_key="book_id",
                                 item_model=Books,
                                 subject_id_key='author_id',
                                 subject_model=Author)
        self.book = pager.get_entry()
        print (f"AuthorkMixin: create-book_pager: book_id={self.book.pk}")
        return book_pager

    def create_pagers(self, book_id):
        # order matters, get book pager (and hence book) first to ascertain the author
        self.book_pager = self.create_book_pager(book_id=book_id)
        # TODO book_pager sets self.book but this is not obvious, make more explicit
        print (f"AuthorMixin::create_pagers: author is '{self.book.author.pk}, {self.book.author}'")
        self.the_pager = self.create_top_level_pager(author_id=self.book.author_id)

