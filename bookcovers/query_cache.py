from django.shortcuts import get_object_or_404

from bookcovers.models import Artist
from bookcovers.models import Artwork
from bookcovers.models import Author
from bookcovers.models import Book
from bookcovers.models import Set
from bookcovers.models import Edition
from bookcovers.models import Cover
from bookcovers.models import Panorama

class QueryCache:
    """'Caches' queries by returning existing object if it matches that requested"""
    @staticmethod
    def transform_slug(slug: str) -> str:
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

        self._panorama_id = None
        self._panorama = None

    def get_subject_identifier(self, subject_id: int=None, name: str=None, slug: str=None) -> dict:
        if subject_id:
            kwargs = {'pk': subject_id}
        elif name:
            kwargs = {'name': name}
        elif slug:
            slug = self.transform_slug(slug)
            kwargs = {'name': slug}  # should this be slug not name?
        # TODO default or exception if no value supplied

        for key, value in kwargs.items():
            print(f"key {key} is '{value}'")
        return kwargs

    def artwork(self, artwork: object=None, artwork_id: int=None) -> object:
        """
        Set artwork and artist of artwork.
        Use artwork object provided.
        or
        Query database if artwork has changed (or not set).

        :param artwork: artwork object, when provided this object is used to set artwork
        or
        :param artwork_id:     primary key for artwork, if different than current artwork, query database
        :return:
        """
        if artwork is not None:
            # use this artwork object
            self._artwork = artwork
            self._artwork_id = artwork.artwork_id
        else:
            # if artwork has changed perform query
            if artwork_id != self._artwork_id or self._artwork is None:
                self._artwork_id = artwork_id
                self._artwork = get_object_or_404(Artwork.objects.select_related('artist'), artwork_id=artwork_id)
        #print(f"QueryCache::artwork: now artwork is {hex(id(self._artwork))}. b4 self.artist")
        self.artist(artist=self._artwork.artist)
        return self._artwork

    def artist(self, artist: object=None, pk: int=None, name: str=None, slug: str=None) -> object:
        """
        Set artist.
        Use artist object provided.
        or
        Query database if artist has changed (or not set).
        Use any of pk, name, or slug according to which has been provided

        :param artist: artist object, when provided this object is used to set artist
        or
        :param pk:     artist_id, if different than current artist, query database
        :param name:    artist name, eg "Bruce Pennington"
        :param slug:    slug, eg "Bruce-Pennington"
        :return:
        """
        #print(f"QueryCache::artist: artist is {artist}, pk is {pk}, name is {name}, slug is {slug}")
        #print(f"QueryCache::artist: _artist_id={self._artist_id}")
        artist_id = pk
        if artist is not None:
            # use this artist object
            self._artist = artist
            self._artist_id = artist.pk
        else:
            # if artist has changed perform query
            if artist_id != self._artist_id or self._artist is None:
                kwargs = self.get_subject_identifier(subject_id=artist_id, name=name, slug=slug)
                self._artist = get_object_or_404(Artist, **kwargs)
                self._artist_id = self._artist.pk
        #print(f"QueryCache::artist: now _artist_id is {self._artist_id}")
        return self._artist

    def book(self, book: object=None, book_id: int=None) -> object:
        if book is not None:
            # use this book object
            self._book = book
            self._book_id = book.book_id
        else:
            # if book has changed perform query
            if book_id != self._book_id or self._book is None:
                self._book_id = book_id
                self._book = get_object_or_404(Book.objects.select_related('author'), book_id=book_id)
        #print(f"QueryCache::book: now book is {hex(id(self._book))}")
        self.author(author=self._book.author)
        return self._book

    def author(self, author: object=None, pk: int=None, name: str=None, slug: str=None) -> object:
        author_id = pk
        if author is not None:
            # use this author object
            self._author = author
            self._author_id = author.pk
        else:
            # if author has changed perform query
            if author_id != self._author_id or self._author is None:
                kwargs = self.get_subject_identifier(subject_id=author_id, name=name, slug=slug)
                self._author = get_object_or_404(Author, **kwargs)
                self._author_id =  self._author.pk
        return self._author

    # TODO further optimization can be achieved by adding query by author and artist
    def set(self, set_id: int) -> object:
        """Set set and author and artist for set"""
        #print(f"QueryCache::set: set object is {hex(id(self._set))}")
        #print(f"QueryCache:set: set_id={set_id}")
        if set_id != self._set_id or self._set is None:
            self._set_id = set_id
            self._set = get_object_or_404(Set.objects.select_related('author','artist'), set_id=set_id)
        #print(f"QueryCache::set: now set object is {hex(id(self._set))}")
        self.author(author=self._set.author)
        self.artist(artist=self._set.artist)
        return self._set

    def edition(self, edition_id: int) -> object:
        """set edition and artwork for edition"""
        edition = get_object_or_404(Edition.objects.select_related('theCover','thePrintRun','book',
                                    'theCover__artwork','theCover__artwork__artist','book__author'),
                                    edition_id=edition_id)
        self.book(book=edition.book)
        try:
            self.artwork(artwork=edition.theCover.artwork)
        except Cover.DoesNotExist:
            self._artwork = None
        return edition

    def panorama(self, pk: int=None) -> object:
        if pk != self._panorama_id or self._panorama is None:
            self._panorama_id = pk
            self._panorama = get_object_or_404(Panorama.objects.select_related('artist'), pk=pk)
        return self._panorama