
from django.views.generic import ListView
from django.views.generic import DetailView

from bookcovers.cover_querys import CoverQuerys
from bookcovers.base_views import SubjectList
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
        # TODO why can't we use artist setter here?
        #print (f"ArtistArtworks::setup: artist_id={self.artist_id} name='{self.name}' slug='{self.slug}'")

    def set_list(self):
        set_list = CoverQuerys.artist_set_list(artist_id=self.artist.pk)
        return set_list

    def get_queryset(self):
        self.the_pager = self.create_top_level_pager(artist_id=self.artist_id, name=self.name, slug=self.slug)
        # get the artist to display
        self.artist = self.the_pager.get_entry()
        self.signature_exists()
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
        edition = self.query_cache.edition(edition_id=self.cover_list[0]['edition__pk'])
        print(f"Artwork: get_object artwork.name={self.artwork.name}")
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
        self.detail['to_page_view_name'] = 'artwork'
        self.detail['list_view_name'] = 'artworks'

    def get_object(self, queryset=None):
        edition = self.query_cache.edition(edition_id=self.edition_id)
        self.create_pagers(artwork_id=edition.theCover.artwork.pk)
        print(f"ArtworkEdition: get_object artwork.name={self.artwork.name}")
        self.cover_list = CoverQuerys.all_covers_for_artwork(self.artwork)
        return edition


# http:<host>/bookcovers/artwork/set/edition/<edition_id>
class ArtworkSetEdition(Artwork):
    """
        given the edition id, displays detail for the edition and thumbnails for the associated editions in the set
    """
    template_name = 'bookcovers/set_edition.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        self.detail['list_view_name'] = 'artwork_set_editions'
        self.detail['view_name'] = 'artwork_set_edition'
        self.detail['to_page_view_name'] = 'artwork_set_detail'
        print (f"ArtworkSetEdition::setup edition_id is '{self.edition_id}'")

    def get_object(self, queryset=None):
        edition = self.query_cache.edition(edition_id=self.edition_id)
        set, self.cover_list = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)
        self.set_pager = self.create_set_pager(set_id=set.pk)
        self.the_pager = self.create_top_level_pager(artist_id=edition.theCover.artwork.artist_id)
        self.edition = edition
        return edition


# http:<host>/bookcovers/artwork/detail/set/<set_id>
class ArtworkSetDetail(ArtworkSetEdition):
    """
        given the set id, displays detail for the edition and thumbnails for the associated editions in the set
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.set_id = kwargs.get("set_id", None)
        print (f"ArtworkSetDetail::setup set_id is '{self.set_id}'")

    def get_object(self, queryset=None):
        self.set_pager = self.create_set_pager(set_id=self.set_id)
        # TODO create_set_pager sets self.set but this is not obvious, make more explicit
        set, self.cover_list = CoverQuerys.author_artist_set_cover_list(set_id=self.set.pk)
        edition = self.query_cache.edition(edition_id=self.cover_list[0]['edition_id'])
        self.the_pager = self.create_top_level_pager(artist_id=edition.theCover.artwork.artist_id)
        self.edition = edition
        return edition


# http:<host>/bookcovers/artworks/<artwork_id>
class Artworks(ArtistMixin, ListView):
    """
        displays all book covers using the same artwork, eg
        'Dune' and 'The Three Stigmata of Palmer Eldritch' by BP
        or all book covers by same artist for the same title, eg two versions of "Decision at Doona" by BP
    """
    template_name = 'bookcovers/artworks.html'
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
        self.signature_exists()
        self.web_title = self.artist.name
        #print (f"ArtistSets:get_queryset: artist is '{self.artist.name}'")
        queryset = CoverQuerys.artist_set_covers(artist_id=self.artist.artist_id, return_dict=True)
        return queryset


# http:<host>/bookcovers/artwork/set/editions/<edition_id>
class ArtworkSetEditions(ArtistMixin, ListView):
    """
        given the edition id, displays all the covers for the set
    """
    template_name = 'bookcovers/set_editions.html'

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.edition_id = kwargs.get("edition_id", None)
        print (f"ArtworkSetEditions::setup: edition_id is {self.edition_id}")
        self.detail['view_name'] = 'artwork_set_edition'
        self.detail['to_page_view_name'] = 'artwork_set_list'

    def get_queryset(self):
        edition = self.query_cache.edition(edition_id=self.edition_id)
        print(f"ArtworkSetEditions::get_queryset author id is '{edition.book.author_id}'")
        print(f"ArtworkSetEditions:get_queryset artist id is '{edition.theCover.artwork.artist_id}'")
        set, queryset = CoverQuerys.author_artist_set_cover_list(author_id=edition.book.author_id,
                                                                   artist_id=edition.theCover.artwork.artist_id)

        self.the_pager = self.create_top_level_pager(artist_id=edition.theCover.artwork.artist_id)
        self.artwork = edition.theCover.artwork
        self.set_pager = self.create_set_pager(set_id=set.pk)
        return queryset

# http:<host>/bookcovers/artwork/list/set/<set_id>
class ArtworkSetList(ArtworkSetEditions):
    """
        given the set idm displays all the covers for the set
    """
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.set_id = kwargs.get("set_id", None)
        print (f"ArtworkSetList::setup set_id is '{self.set_id}'")

    def get_queryset(self):
        self.set_pager = self.create_set_pager(set_id=self.set_id)
        # TODO create_set_pager sets self.set but this is not obvious, make more explicit
        set, queryset = CoverQuerys.author_artist_set_cover_list(set_id=self.set.pk)
        edition = self.query_cache.edition(edition_id=queryset[0]['edition_id'])
        self.the_pager = self.create_top_level_pager(artist_id=edition.theCover.artwork.artist_id)
        self.edition = edition
        return queryset
