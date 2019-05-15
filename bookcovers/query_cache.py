from django.shortcuts import get_object_or_404
from bookcovers.models import Artist
from bookcovers.models import Artwork
from bookcovers.models import Author
from bookcovers.models import Book
from bookcovers.models import Set
from bookcovers.models import Edition

class QueryCache:
    @staticmethod
    def transform_slug(slug):
        slug = slug.replace('__', '%')
        slug = slug.replace('-', ' ')
        slug = slug.replace('%', '-')
        return slug

    def __init__(self):
        self._artist = None
        self._artist_id = None
        self._artwork_id = None
        self._artwork = None
        print(f"QueryCache:init: self._artwork_id={self._artwork_id}")

        self._author = None
        self._author_id = None
        self._book_id = None
        self._book = None
        print(f"QueryCache:init: self._book_id={self._book_id}")

        self._set_id = None
        self._set = None
        print(f"QueryCache:init: self._set_id={self._set_id}")

    def get_subject_identifier(self, subject_id=None, name=None, slug=None):
        if subject_id:
            kwargs = {'pk': subject_id}
        elif name:
            kwargs = {'name': name}
        elif slug:
            slug = self.transform_slug(slug)
            kwargs = {'name': slug}
        # TODO default or exception if no value supplied

        for key, value in kwargs.items():
            print(f"key {key} is '{value}'")

        return kwargs

    def artwork(self, artwork=None, artwork_id=None):
        if artwork is not None:
            self._artwork = artwork
            self._artwork_id = artwork.artwork_id
        else:
            if artwork_id != self._artwork_id or self._artwork is None:
                self._artwork_id = artwork_id
                self._artwork = get_object_or_404(Artwork.objects.select_related('artist'), artwork_id=artwork_id)
        print(f"QueryCache::artwork: now artwork is {hex(id(self._artwork))}")
        self.artist(artist= self._artwork.artist)
        return self._artwork

    def artist(self, artist=None, pk=None, name=None, slug=None):
        artist_id = pk
        if artist is not None:
            self._artist = artist
            self._artist_id = artist.pk
        else:
            if artist_id != self._artist_id or self._artist is None:
                kwargs = self.get_subject_identifier(subject_id=artist_id, name=name, slug=slug)
                self._artist = get_object_or_404(Artist, **kwargs)
                self._artist_id = self._artist.pk
        return self._artist

    def book(self, book=None, book_id=None):
        if book is not None:
            self._book = book
            self._book_id = book.book_id
        else:
            if book_id != self._book_id or self._book is None:
                self._book_id = book_id
                self._book = get_object_or_404(Book.objects.select_related('author'), book_id=book_id)
        print(f"QueryCache::book: now book is {hex(id(self._book))}")
        self.author(author=self._book.author)
        return self._book

    def author(self, author=None, pk=None, name=None, slug=None):
        author_id = pk
        if author is not None:
            self._author = author
            self._author_id = author.pk
        else:
            if author_id != self._author_id or self._author is None:
                kwargs = self.get_subject_identifier(subject_id=author_id, name=name, slug=slug)
                self._author = get_object_or_404(Author, **kwargs)
                self._author_id =  self._author.pk
        return self._author

    # TODO further optimization can be achieved by adding query by author and artist
    def set(self, set_id):
        print(f"QueryCache::set: set is {hex(id(self._set))}")
        print(f"QueryCache:set: set_id={set_id}")
        if set_id != self._set_id or self._set is None:
            self._set_id = set_id
            self._set = get_object_or_404(Set.objects.select_related('author','artist'), set_id=set_id)
        print(f"QueryCache::set: now set is {hex(id(self._set))}")
        self.author(author=self._set.author)
        self.artist(artist=self._set.artist)
        return self._set

    def edition(self, edition_id):
        edition = get_object_or_404(Edition.objects.select_related('theCover','thePrintRun','book',
                                    'theCover__artwork','theCover__artwork__artist','book__author'),
                                    edition_id=edition_id)
        #self.author(edition.book.author)
        self.book(book=edition.book)
        self.artwork(artwork=edition.theCover.artwork)
        return edition