from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView

from bookcovers.models import Editions
from bookcovers.cover_querys import CoverQuerys
from bookcovers.views import SubjectList

from .view_mixin import ArtistMixin

# ArtistList -> ArtistArtworks -> Artwork
# http:<host>/bookcovers/artists/
class ArtistList(SubjectList):
    template_name = 'bookcovers/artist_list.html'

    def __init__(self):
        self.title = "Artists"

    def get_queryset(self):
        queryset = CoverQuerys.artist_list()
        return queryset


# http:<host>/bookcovers/artist/<artist_id>
# http:<host>/bookcovers/artist/<artist%20name>
# http:<host>/bookcovers/artist/<artist-slug>
class ArtistArtworks(ArtistMixin, ListView):
    """
    displays list of books with covers by this artist as thumbnails
    :param request:
    one of
    :param artist_id:   ex: /bookcovers/artist/6/
    :param name:        ex: /bookcovers/artist/Jim%20Burns/
    :param slug:        ex: /bookcovers/artist/Jim-Burns/
    :return:
    """
    template_name = 'bookcovers/artist_artworks.html'
    context_object_name = 'cover_list'      # template context


    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.artist_id = kwargs.get("artist_id", None)
        self.name = kwargs.get("name", None)
        self.slug = kwargs.get("slug", None)
        self._artist = None
        print (f"in setup: artist_id={self.artist_id}")

    def set_list(self):
        set_list = CoverQuerys.artist_set_list(artist_id=self.artist.pk)
        return set_list

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(artist_id=self.artist_id, name=self.name, slug=self.slug)
        # get the artist to display
        self.artist = self.the_pager.get_entry()
        self.web_title = self.artist.name
        queryset = CoverQuerys.artist_cover_list(artist=self.artist)
        return queryset


# http:<host>/bookcovers/artwork/<artwork_id>
class Artwork(ArtistMixin, DetailView):
    template_name = 'bookcovers/artwork_cover.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.artwork_id = kwargs.get("artwork_id", None)
        print (f"Artwork:setup artwork id is '{self.artwork_id}'")

    def get_object(self, queryset=None):
        self.create_pagers(artwork_id=self.artwork_id)
        self.cover_list = CoverQuerys.all_covers_for_artwork(self.artwork)
        edition = get_object_or_404(Editions, edition_id=self.cover_list[0]['edition__pk'])
        print(f"ArtworkCover: get_object artwork.name={self.artwork.name}")
        return edition

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cover_list'] = self.cover_list
        return context


# http:<host>/bookcovers/artwork/edition/<edition_id>
class ArtworkEdition(Artwork):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)

    def get_object(self, queryset=None):
        edition = get_object_or_404(Editions, edition_id=self.edition_id)
        print (f"ArtworkEdition: artist is '{edition.theCover.artwork.artist_id}'")
        self.create_pagers(artwork_id=edition.theCover.artwork.pk)
        print(f"ArtworkEdition: get_object artwork.name={self.artwork.name}")
        self.cover_list = CoverQuerys.all_covers_for_artwork(self.artwork)
        return edition

# http:<host>/bookcovers/artwork/set/edition/<edition_id>
# if meaningful make base class of Book without mixin and then inherit with mixin
class ArtworkSetEdition(Artwork):
    template_name = 'bookcovers/set_edition.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        self.detail['list_view_name'] = 'artwork_set_editions'
        self.detail['view_name'] = 'artwork_set_edition'

    def get_object(self, queryset=None):
        edition = get_object_or_404(Editions, edition_id=self.edition_id)
        print (f"ArtworkSetEdition:get_object author id is '{edition.book.author_id}'")
        print (f"ArtworkSetEdition:get_object artist id is '{edition.theCover.artwork.artist_id}'")
        self.create_pagers(artwork_id=edition.theCover.artwork.pk)
        self.cover_list = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)
        self.detail['object'] = edition
        return edition


# http:<host>/bookcovers/artwork/set/editions/<edition_id>
# up to here  want to factor out repetition between book and artwork.
# also ArtworkSetEdtion get_object and ArtworkSetEdtions get_queryset the same - create a method to call
# if meaningful make base class of SetEditions without mixin and then inherit with mixin
class ArtworkSetEditions(ArtistMixin, ListView):
    """
        displays all the covers for the set
    """
    template_name = 'bookcovers/set_editions.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        print (f"ArtworkSetEditions::setup: edition_id is {self.edition_id}")

    def get_queryset(self):
        edition = get_object_or_404(Editions, edition_id=self.edition_id)
        print (f"ArtworkSetEditions:get_object author id is '{edition.book.author_id}'")
        print (f"ArtworkSetEditions:get_object artist id is '{edition.theCover.artwork.artist_id}'")
        self.create_pagers(artwork_id=edition.theCover.artwork.pk)
        queryset = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)
        return queryset

# http:<host>/bookcovers/artworks/<artwork_id>
class ArtworkList(ArtistMixin, ListView):
    """
        displays all book covers using the same artwork, eg
        'Dune' and 'The Three Stigmata of Palmer Eldritch' by BP
        or all book covers by same artist for the same title, eg two versions of "Decision at Doona" by BP
    """
    template_name = 'bookcovers/artwork_list.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.artwork_id = kwargs.get("artwork_id", None)

    def get_queryset(self):
        self.create_pagers(artwork_id=self.artwork_id)
        print (f"ArtworkList: get_queryset artwork.name={self.artwork.name}")
        queryset = CoverQuerys.all_covers_for_artwork(self.artwork)
        return queryset


# http:<host>/bookcovers/artist/<artist%20name>/sets
class ArtistSets(ArtistMixin, ListView):
    """
    displays thumbnails of books by this artist ordered in sets by author
    """
    template_name = 'bookcovers/artist_sets.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.name = kwargs.get("name", None)
        print (f"ArtistSets::setup: artist={self.name}")

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(name=self.name)
        self.artist = self.the_pager.get_entry()
        # TODO pagers set objects but it is not obvious
        self.web_title = self.artist.name
        print (f"ArtistSets:get_queryset: artist is '{self.artist.name}'")
        queryset = CoverQuerys.artist_set_covers(artist_id=self.artist.artist_id, return_dict=True)
        return queryset

# http:<host>/bookcovers/artwork/set/edition/<edition_id>
# if meaningful make base class of Book without mixin and then inherit with mixin
class ArtworkSetEdition(Artwork):
    template_name = 'bookcovers/set_edition.html'
    context_object_name = "edition"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        self.detail['list_view_name'] = 'artwork_set_editions'
        self.detail['view_name'] = 'artwork_set_edition'

    def get_object(self, queryset=None):
        edition = get_object_or_404(Editions, edition_id=self.edition_id)
        print (f"ArtworkSetEdition:get_object author id is '{edition.book.author_id}'")
        print (f"ArtworkSetEdition:get_object artist id is '{edition.theCover.artwork.artist_id}'")
        self.create_pagers(artwork_id=edition.theCover.artwork.pk)
        self.cover_list = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)
        self.detail['object'] = edition
        return edition


# http:<host>/bookcovers/artwork/set/editions/<edition_id>
# up to here  want to factor out repetition between book and artwork.
# also ArtworkSetEdtion get_object and ArtworkSetEdtions get_queryset the same - create a method to call
# if meaningful make base class of SetEditions without mixin and then inherit with mixin
class ArtworkSetEditions(ArtistMixin, ListView):
    """
        displays all the covers for the set
    """
    template_name = 'bookcovers/set_editions.html'
    context_object_name = 'cover_list'      # template context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        print (f"ArtworkSetEditions::setup: edition_id is {self.edition_id}")

    def get_queryset(self):
        edition = get_object_or_404(Editions, edition_id=self.edition_id)
        print (f"ArtworkSetEditions:get_object author id is '{edition.book.author_id}'")
        print (f"ArtworkSetEditions:get_object artist id is '{edition.theCover.artwork.artist_id}'")
        self.create_pagers(artwork_id=edition.theCover.artwork.pk)
        queryset = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)
        return queryset
