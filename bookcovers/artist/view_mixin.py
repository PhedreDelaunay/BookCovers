from django.shortcuts import get_object_or_404

from bookcovers.pagers import ArtistPager
from bookcovers.pagers import ArtworkPager
from bookcovers.pagers import SetPager

from bookcovers.cover_querys import CoverQuerys
from bookcovers.models import Artist
from bookcovers.models import Set
from bookcovers.models import Edition

from bookcovers.view_mixin import TopLevelPagerMixin

class ArtistMixin(TopLevelPagerMixin):

    def __init__(self):
        super().__init__()

        self.subject_list = {
            'title': 'artists',
            'view_name': 'artists',
            'object': None,
        }
        self.subject = {
            'name': 'artist',
            'title': 'artworks',
            'view_name': 'artist_artworks',
            'set_view_name': 'artist_sets',
            'object': None,
        }
        self.detail = {
            'to_page_view_name': 'artwork',
            'view_name': 'artwork',
            'list_view_name': 'artworks',
            'object': None,
        }

    @property
    def artist(self):
        return self._artist

    @artist.setter
    def artist(self, value):
        self._artist = value
        self.subject['object'] = self._artist
        print (f"artist_setter: set subject object artist is {value}")

    @property
    def artwork(self):
        return self._artwork

    @artwork.setter
    def artwork(self, value):
        self._artwork = value
        self.set_artwork_attributes(self._artwork)

    def set_artwork_attributes(self, artwork):
        self.detail['object'] = artwork
        self.web_title = artwork.name
        print(f"set_artwork_attributes: set detail object artwork is {artwork}")
        #self.artist = artwork.artist
        self.artist = artwork.get_creator

    @property
    def edition(self):
        return self._edition

    @edition.setter
    def edition(self, value):
        self._edition = value
        self.set_edition_attributes(self._edition)

    def set_edition_attributes(self, edition):
        print(f"set_edition_attributes: set detail object edition is {edition}")
        self.artwork = edition.theCover.artwork
        self.artist = self.artwork.artist
        self.web_title = self.artist.name
        # must set after artwork attributes
        self.detail['object'] = edition

    def create_top_level_pager(self, artist_id=None, name=None, slug=None):
        print(f"ArtistMixin:create_top_level_pagert: artist_id={artist_id} name='{name}' slug='{slug}'")
        artist_pager = ArtistPager(self.request, self.query_cache,  artist_id=artist_id, name=name, slug=slug)
        return artist_pager

    def create_artwork_pager(self, artwork_id):
        # book cover pager
        page_number = self.request.GET.get('page')
        print(f"ArtworkMixin: create_book_pager - page number is '{page_number}'")

        pager = ArtworkPager(self.query_cache, page_number=page_number, item_id=artwork_id)
        artwork_pager = pager.pager(book_cover_query=CoverQuerys.artist_cover_list,
                                 item_id_key="artwork_id")
        # subject_id_key = 'artist_id',
        # subject_model = Artist
        self.artwork = pager.get_entry()
        print (f"ArtworkMixin: create_book_pager: artwork_id={self.artwork.pk}")
        print(f"ArtworkMixin: create_book_pager: artwork.name={self.artwork.name}")
        return artwork_pager

    def create_set_pager(self, set_id):
        # book cover pager
        page_number = self.request.GET.get('page')
        print(f"ArtworkMixin: create_set_pager - page number is '{page_number}'")

        pager = SetPager(self.query_cache, page_number=page_number, item_id=set_id)
        set_pager = pager.pager(set_query=CoverQuerys.artist_set_list,
                                item_id_key="set_id",
                                item_model=Set,
                                subject_model=Artist)
        self.set = pager.get_entry()
        return set_pager

    def create_pagers(self, artwork_id):
        # order matters, get book pager (and hence artwork) first to ascertain the artist
        self.book_pager = self.create_artwork_pager(artwork_id=artwork_id)
        # TODO book_pager sets self.artwork but this is not obvious, make more explicit
        print (f"ArtworkMixin::create_pagers: artist is '{self.artwork.artist.pk}, {self.artwork.artist_id}'")
        self.the_pager = self.create_top_level_pager(artist_id=self.artwork.artist_id)

    def get_edition(self, edition_id):
        edition = get_object_or_404(Edition.objects.select_related('theCover','thePrintRun','book',
                                    'theCover__artwork','theCover__artwork__artist','book__author'),
                                    edition_id=edition_id)
        return edition