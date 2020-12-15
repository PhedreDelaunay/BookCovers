import pprint

from django.db.models import F
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Max

from bookcovers.models import Author
from bookcovers.models import Artist
from bookcovers.models import Artwork
from bookcovers.models import Book
from bookcovers.models import Cover
from bookcovers.models import Edition
from bookcovers.models import Set
from bookcovers.models import SetExceptions
from bookcovers.models import BookSeries
from bookcovers.models import PrintRun
from bookcovers.models import Panorama
from bookcovers.models import Artbook
from bookcovers.models import ArtbookIndex
from bookcovers.debug_helper import DebugHelper


class CoverQuerys:
    """Gathers all queries into one place, along with query_cache"""
    @staticmethod
    def artist_list():
        inner_queryset = Artwork.objects. \
            filter(theCover__flags__lt=256). \
            values_list('artwork_id', flat=True)

        artist_list = Artist.objects. \
            filter(theArtwork__in=inner_queryset). \
            values('artist_id', 'name'). \
            order_by('name'). \
            distinct()
        # print(artist_list.query)
        # print(artist_list.count())
        return artist_list

    @staticmethod
    def artist_cover_list(artist):
        """
        :param artist:   artist model instance
        :return:
        """
        print("artist is {}".format(artist.name))
        aka_inner_queryset = Artist.objects.filter(theArtist_aka__artist_aka_id=artist.pk)
        # print (aka_inner_queryset.query)
        # print (aka_inner_queryset)

        # up to here -
        # tried setting a high bit field on these covers in fixtures to see if it helps
        # have edited fixtures to set to 1028
        # the problem is that the artwork_id ends up in the exclusion list and so is excluded
        #         cover_list = Artworks.objects. \
        #             filter(Q(artist=artist) | Q(artist__in=aka_inner_queryset)). \
        #             filter(theCover__flags__lt=256). \
        #             filter(theCover__book=F('book')). \
        #             exclude(theCover__flags=F('theCover__flags').bitor(4)). \
        #             values('theCover__cover_id',
        #                    'theCover__edition',
        #                    'theCover__flags',
        #                    'theCover__flags',
        #                    'book',
        #                    'artwork_id',
        #                    'book__author__name',
        #                    'book__title',
        #                    'theCover__cover_filename',
        #                    'year') \
        #             .order_by('year', 'artwork_id') \
        #             .distinct()

        # edition_id not null in fixtures because model set to one-to-one
        # problem is exacerbated by 2 cover records with edition=NULL
        # 646/632 TheChrysalids, 640/460 Neuromancer7
        # these are minor variants of the cover not the artwork
        # functionality is that both covers are shown in artist list but not title list
        # can't see any difference in TheChrysalids,
        # Neuromancer is slight difference in colours which is interesting but not important
        # how do we want to handle this

        # currently have cover->edition one-to-one
        # multiple editions will use same cover - how is this currently handled from a data point of view?
        # print runs I think
        #
        # Have abandoned the attempt.  Either keep using isvariant or replace 4 with 1024


    # this is the working filter without the bitflags
    #    filter(Q(artist=artist) | Q(artist__in=aka_inner_queryset)). \
    #    filter(Q(theCover__flags__lt=256) & Q(theCover__is_variant=False) & Q(theCover__book=F('book'))). \

        cover_list = Artwork.objects. \
            filter(Q(artist=artist) | Q(artist__in=aka_inner_queryset)). \
            filter(Q(theCover__flags__lt=256) & Q(theCover__is_variant=False) & Q(theCover__book=F('book'))). \
            values('theCover__cover_id',
                   'theCover__edition',
                   'theCover__flags',
                   'theCover__flags',
                   'book',
                   'artwork_id',
                   'book__author__name',
                   'book__title',
                   'theCover__cover_filename',
                   'year') \
            .order_by('year', 'artwork_id')

        if artist.name.lower() == "artist unknown":
            for cover in cover_list:
                author_directory = cover['book__author__name'].replace(" ","").replace(".","")
                cover['book__author__name'] = f"{author_directory}/"
        #print(f"artist_cover_list.query is '{cover_list.query}'")
        # print("len(cover_list) is {}".format(len(cover_list)))
        return cover_list

    @staticmethod
    def author_list():
        """
        gets the list of authors that have books with covers in the database
        filters out covers that aren't ready yet (eg data exists but not yet scanned)|
        the database holds many authors that aren't relevant to this website - todo clean up database

        :return: dict queryset of authors
        """
        # https://docs.djangoproject.com/en/2.0/topics/db/queries/#backwards-related-objects

        # https://docs.djangoproject.com/en/2.0/ref/models/querysets/
        # If you only pass in a single field, you can also pass in the flat parameter.
        # If True, this will mean the returned results are single values, rather than one-tuples.

        # covers -> editions is one-to-one
        inner_queryset = Edition.objects \
            .filter(theCover__flags__lt=256) \
            .values_list('edition_id', flat=True)
        # https://docs.djangoproject.com/en/2.0/ref/models/querysets/
        # flat=True returns a list of single items for a single field

        # print ("author_list: inner_queryset is:")
        # print(inner_queryset.query)
        # print("count inner_queryset is", inner_queryset.count())
        # print("len inner_queryset is", len(inner_queryset))
        # print(inner_queryset)

        # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#in
        # need to clean database

        author_list = Author.objects \
            .filter(author_id=F('theBook__author')) \
            .filter(theBook__theEdition__edition_id__in=inner_queryset) \
            .values('author_id', 'name') \
            .order_by('name') \
            .distinct()

        # print(author_list.query)
        # print(author_list.count())
        return author_list


    @staticmethod
    def books_for_author(author):
        print("author is {}".format(author.name))
        aka_inner_queryset = Author.objects.filter(theAuthor_aka__author_aka_id=author.pk)

        book_list = Book.objects \
            .filter(Q(author=author) | Q(author__in=aka_inner_queryset)) \
            .filter(Q(theCover__flags__lt=256)) \
            .values('book_id','title','copyright_year') \
            .distinct() \
            .order_by('copyright_year')
        return book_list

    @staticmethod
    def all_covers_of_all_books_for_author(author, author_id=None, all=True):
        """
        gets all covers of all books for this author
        :param author: author object to fetch covers for, required to get real name
        :param all: True = return all covers for all books
                    False = eliminates duplicate cover entries, where the same file is used for multiple cover records
        :return: dict queryset to fetch all covers of all books for this author
        """
        if not author_id:
            author_id = author.pk
            print("author is {}".format(author.name))
        print (f"author_id is {author_id}")
        aka_inner_queryset = Author.objects.filter(theAuthor_aka__author_aka_id=author_id)

        # this returns all covers for all books by this author
        all_cover_list = Book.objects \
            .filter(Q(author=author_id) | Q(author__in=aka_inner_queryset)) \
            .filter(Q(theCover__flags__lt=256)) \
            .values('book_id',
                    'theCover__edition__pk',
                   'theCover__artwork__artist__cover_filepath',
                   'theCover__cover_filename',
                   'title',
                   'copyright_year',
                   'theCover__artwork__year') \
            .order_by('copyright_year',
                      'book_id',
                      'theCover__artwork__year')

        # .exclude(Q(pk=F('theCover__book__pk')) & Q(theCover__edition__pk__isnull=True)) \

        # this eliminates duplicate cover entries, where the same file is used for multiple cover records
        # TODO: not anymore, gives the same result as above
        # eg John Wyndham, The Chrysalids, by Brian Cronin covers: 645, 646
        dedup_cover_list = Book.objects \
            .filter(Q(author=author_id) | Q(author__in=aka_inner_queryset)) \
            .filter(Q(theCover__flags__lt=256)) \
            .values('book_id',
                    'theCover__edition__pk',
                   'theCover__artwork__artist__cover_filepath',
                   'theCover__cover_filename',
                   'title',
                   'copyright_year',
                   'theCover__artwork__year') \
            .order_by('copyright_year',
                      'book_id',
                      'theCover__artwork__year') \
            .distinct ()

        if all:
            cover_list = all_cover_list
        else:
            cover_list = dedup_cover_list

        # https://stackoverflow.com/questions/3897499/check-if-value-already-exists-within-list-of-dictionaries
        # use list comprehension to test if there are any unknown artists in this author's cover collection
        if any(cover['theCover__artwork__artist__cover_filepath'] == 'BookCovers/Images/Unknown/' for cover in cover_list):
            #print (f"author {author.name}: has unknown cover")
            print (f"author {author_id}: has unknown cover")

            try:
                real_author = Author.objects.get(Q(theAuthor_aka__real_name=1) &
                                                 (Q(theAuthor_aka__author_aka_id=author_id)
                                                    | Q(theAuthor_aka__author_id=author_id)))
                print (f"real author name is {real_author.name}")
            except Author.DoesNotExist as e:
                real_author = author
                # TODO if author none fetch author then don't need to in test?

            author_directory = real_author.name.replace(" ", "").replace(".","")
            for cover in cover_list:
                if cover['theCover__artwork__artist__cover_filepath'] == "BookCovers/Images/Unknown/":
                    cover['theCover__artwork__artist__cover_filepath'] = f"BookCovers/Images/Unknown/{author_directory}/"
        else:
            #print (f"author {author.name}: has no unknown covers")
            print (f"author {author_id}: has no unknown covers")

        #print (list(cover_list))
        #print(f"django author cover_list query is\n{cover_list.query}")
        # print("len(cover_list) is {}".format(len(cover_list)))
        return cover_list

    @staticmethod
    def all_covers_for_title(book):
        """
        list all covers for this title
        :param book_id:
        :return:
        """

        #strAuthorCoverSQL = ("SELECT artists.cover_filepath, AW.artwork_id, BC.*, BE.print_year, C.country_id, C.display_order "
        #                    "FROM artists, artworks as AW, covers AS BC, editions AS BE, countries AS C "
        #
        #                    "WHERE BC.flags < 256 AND BC.book_id = %s AND BC.book_id = BE.book_id "
        #                    "AND BC.edition_id = BE.edition_id "
        #                    "AND AW.artwork_id = BC.artwork_id AND artists.artist_id = AW.artist_id "
        #                    "AND C.country_id = BE.country_id "
        #                    "ORDER BY C.display_order, BE.print_year")

        inner_queryset = Book.objects.filter(book_id=book.book_id).values_list('theEdition__edition_id', flat=True)


        # title_cover_list = Covers.objects \
        #     .filter(book=book, flags__lt=256) \
        #     .filter(edition__in=inner_queryset) \
        #     .values('artwork__artist__cover_filepath',
        #             'cover_filename',
        #             'book__title',
        #             'book__author__name',       # needed for unknown artists
        #             'edition__pk',
        #             'edition__country',
        #             'edition__country__display_order',
        #             'edition__print_year') \
        #     .order_by('edition__country__display_order','edition__print_year')

        # pk is book_id
        title_cover_list = Cover.objects \
            .filter(book=book, flags__lt=256) \
            .filter(edition__in=inner_queryset) \
            .values('cover_filename',
                    'book__author__name',       # needed for unknown artists
                    'edition_id',
                    'edition__country',
                    'edition__print_year',
                    display_order=F('edition__country__display_order'),
                    book_title=F('book__title'),
                    cover_filepath=F('artwork__artist__cover_filepath')) \
            .order_by('display_order','edition__print_year')
        return title_cover_list

    @staticmethod
    def all_covers_for_artwork(artwork):
        """
        list all covers with this artwork
        :param artwork: model instance of artwork to fetch covers for
        :return:
        """

        # we need to cover all these scenarios
        # list covers for artwork/title
        # Time Enough for Love, book_id=25, artist_id=2; artwork_id=22, edition id = 206, 14
        # Decision at Doona, book_id=82, artist_id=2, artwork_id=74, 452, edition_id=89,640
        # Dune, book_id=7, artist_id=2; artwork_id=6 edition|-id=6, book_id=6 artwork_id=6, edition_id=7

        covers = Cover.objects \
                .filter(Q(artwork_id=artwork.pk) |
                        Q(artwork__artist_id=artwork.artist_id, artwork__book_id=artwork.book_id)) \
                .filter(flags__lt = 256) \
                .values('cover_id',
                        'book__pk',
                        'book__title',
                        'artwork__pk',
                        'edition__pk',
                        'artwork__artist__pk',
                        'cover_filename',
                        cover_filepath=F('artwork__artist__cover_filepath'), \
                        author=F('book__author__name'))

        print (f"all_covers_for_artwork: covers.query is\n{covers.query}")
        return covers

    @staticmethod
    def artist_set_list(artist_id):
        """
        gets all the sets for this artist
        :param artist_id:
        :return:
        """
        # use .values to return ValuesQuerySet which looks like list of dictionaries
        #artist_set_list = Sets.objects.filter(author_id=author).values()

        artist_set_list = Set.objects.filter(artist_id=artist_id). \
                            values("set_id", "series_id", "author_id", "artist_id", "imprint_id",
                                    "description", "panorama_id", 'artist__name'). \
                            order_by('author__name')

        # SELECT sets.*, artists.name FROM sets, artists WHERE sets.artist_id = %d AND sets.artist_id = artists.artist_id
        return artist_set_list

    @staticmethod
    def artist_set_covers(artist_id=None, return_dict=True):
        """
        gets all the covers in all the sets for this artist, ordered by author and volume
        :param artist_id:
        :param return_dict:
        :return:
        """
        series_list = Set.objects.filter(artist=artist_id).values_list('series_id', flat=True).distinct()
        # if len(series_list) > 0:
        #     print(f"artist_set_covers: series - {list(series_list)})")
        #     print(f"artist_set_covers: length {len(series_list)}")

        inner_queryset_cover_list = BookSeries.objects. \
            filter(series__in=series_list). \
            filter(book__theCover__artwork__artist__pk=artist_id). \
            values_list('book__theCover__pk', flat=True). \
            order_by('volume')
        # if len(series_list) > 0:
        #     print (f"artist_set_covers: - inner_queryset_cover_list - {inner_queryset_cover_list.query}")
        #     print (f"artist_set_covers: {list(inner_queryset_cover_list)})")
        #     print(f"artist_set_covers: length {len(inner_queryset_cover_list)}")

        inner_queryset_exceptions = SetExceptions.objects. \
            values_list('cover', flat=True)

        cover_list = Cover.objects. \
            filter(cover_id__in=inner_queryset_cover_list). \
            filter(book__theBooksSeries__series_id__in=series_list). \
            exclude(cover_id__in=inner_queryset_exceptions). \
            filter(is_variant=False, flags__lt=256). \
            order_by('book__author', 'book__theBooksSeries__volume')
        if len(series_list) > 0:
            print (f"artist_set_covers: {cover_list.query}")
            print (f"artist_set_covers: {list(cover_list)}")
            print (f"artist_set_covers: length {len(cover_list)}")

        if return_dict:
            set_cover_list = cover_list. \
                values('cover_id',
                       'cover_filename',
                       'artwork_id',
                       'edition_id',
                       'book_id',
                       'book__title',
                       author_id=F('book__author__pk'),
                       author_name=F('book__author__name'),
                       cover_filepath=F('artwork__artist__cover_filepath'),
                       )
        else:
            set_cover_list = cover_list. \
                select_related('book', 'artwork')
        # if len(series_list) > 0:
        #     print (f"artist_set_covers: {list(set_cover_list)}")
        return set_cover_list


    @staticmethod
    def book_list():
        book_list = Book.objects.filter(theCover__flags__lt=256).values('book_id').order_by('book_id')
        print (f"book_list.query is {book_list.query}")
        return book_list


    @staticmethod
    def author_set_list(author_id):
        """
        gets all the sets for this author
        :param author_id:
        :return:
        """
        # use .values to return ValuesQuerySet which looks like list of dictionaries
        #set_list = Sets.objects.filter(author_id=author).values()

        author_set_list = Set.objects.filter(author_id=author_id) \
                     .values("set_id", "series_id", "author_id", "artist_id", "imprint_id",
                             "description", "panorama_id", 'artist__name')
        # SELECT sets.set_id, sets.series_id, sets.author_id, sets.artist_id, sets.imprint_id, sets.description, sets.panorama_id
        # FROM sets LEFT OUTER JOIN artists on sets.artist_id = artists.artist_id WHERE sets.author_id = '15';
        return author_set_list

    @staticmethod
    def author_set_covers(author_id=None, return_dict=True):
        """
        gets all the covers in all the sets for this author, ordered by artist and volume
        :param author_id:
        :param return_dict:
        :return:
        """
        series_list = Set.objects.filter(author=author_id).values_list('series_id', flat=True).distinct()
        # if len(series_list) > 0:
        #     print(f"author_set_covers: {list(series_list)})")
        #     print(f"author_set_covers: length {len(series_list)}")

        # set includes artist,  we want covers with that artist
        inner_queryset_cover_list = BookSeries.objects. \
            filter(series__in=series_list). \
            filter(series__theSet__artist__pk=F('book__theCover__artwork__artist__pk')). \
            values_list('book__theCover__pk', flat=True). \
            order_by('volume')
        # if len(series_list) > 0:
        #     print (f"author_set_covers: {inner_queryset_cover_list.query}")
        #     print (f"author_set_covers: {list(inner_queryset_cover_list)})")
        #     print(f"author_set_covers: length {len(inner_queryset_cover_list)}")

        inner_queryset_exceptions = SetExceptions.objects. \
            values_list('cover', flat=True)

        cover_list = Cover.objects. \
            filter(cover_id__in=inner_queryset_cover_list). \
            filter(book__theBooksSeries__series_id__in=series_list). \
            exclude(cover_id__in=inner_queryset_exceptions). \
            filter(is_variant=False, flags__lt=256)
        # if len(series_list) > 0:
        #     print (f"author_set_covers: {cover_list.query}")
        #     print (f"author_set_covers: {list(cover_list)}")
        #     print (f"author_set_covers: length {len(cover_list)}")

        if return_dict:
            # 1 query 0.45MS
            set_cover_list = cover_list. \
                order_by('artwork__artist', 'book__theBooksSeries__volume'). \
                values('cover_id',
                       'cover_filename',
                       'artwork_id',
                       'edition_id',
                       'book__pk',
                       'book__title',
                       artist_name=F('artwork__artist__name'),
                       cover_filepath=F('artwork__artist__cover_filepath'),
                       )
        else:
            # 19 queries in 2.4MS
            set_cover_list = cover_list. \
                order_by('artwork__artist', 'book__theBooksSeries__volume'). \
                select_related('book','artwork')
        # if len(series_list) > 0:
        #     print (f"author_set_covers: {list(set_cover_list)}")
        return set_cover_list

    @staticmethod
    def series_covers_by_artist(series_id, artist_id=None, return_dict=True):
        """
        gets all the covers by this artist in the set for this series

        :param series_id:
        :param return_dict:
        :return:
        """

        inner_queryset_exceptions = SetExceptions.objects. \
            values_list('cover', flat=True)
        #print(f"series_covers: {list(inner_queryset_exceptions)}")
        #print(f"series_covers: length {len(inner_queryset_exceptions)}")

        # this gives us list of covers in correct order but still includes exceptions
        # if you exclude here too many records are excluded
        inner_queryset_cover_list = BookSeries.objects. \
            filter(series=series_id). \
            filter(book__theCover__artwork__artist__pk=artist_id). \
            values_list('book__theCover__pk', flat=True)
        #print(f"series_covers: inner -{list(inner_queryset_cover_list)}")
        #print(f"series_covers: inner -length {len(inner_queryset_cover_list)}")

        cover_list = Cover.objects. \
            filter(book__theBooksSeries__series=series_id).\
            exclude(cover_id__in=inner_queryset_exceptions). \
            filter(cover_id__in=inner_queryset_cover_list). \
            filter(is_variant=False, flags__lt=256)

        #print (f"set_covers: {cover_list.query}")
        #print (f"series_covers: {list(cover_list)}")
        #print (f"series_covers: length {len(cover_list)}")

        if return_dict:
            # series_cover_list = cover_list. \
            #     order_by('book__theBooksSeries__volume'). \
            #     values('artwork__artist__name',
            #            'artwork__artist__cover_filepath',
            #            'cover_id',
            #            'cover_filename',
            #            'artwork_id',
            #            'edition_id',
            #            'book__pk',
            #            'book__title')

               series_cover_list = cover_list. \
                    order_by('book__theBooksSeries__volume'). \
                    values('cover_id',
                           'cover_filename',
                           'artwork_id',
                           'edition_id',
                           book_title=F('book__title'),
                           cover_filepath=F('artwork__artist__cover_filepath'))
        else:
            series_cover_list = cover_list. \
                order_by('artwork__artist', 'book__theBooksSeries__volume'). \
                select_related('book','artwork')

        #DebugHelper.print_dict_list(list(series_cover_list))
        # print(f"series_covers: length {len(series_cover_list)}")
        return series_cover_list

    @staticmethod
    def author_artist_set_cover_list(set_id=None, author_id=None, artist_id=None):
        # get set record if necessary
        if not author_id or not artist_id:
            set = get_object_or_404(Set, pk=set_id)
            artist_id = set.artist_id
        else:
            # assumes there is only 1 unique set for this author and artist
            set = get_object_or_404(Set, author=author_id, artist_id=artist_id)
            print(f"author_artist_set_cover_list: set is {set.pk}, series is {set.series_id}")

        set_cover_list = CoverQuerys.series_covers_by_artist(series_id=set.series_id, artist_id=artist_id)
        return (set, set_cover_list)

    @staticmethod
    def print_history(print_run_id):
        print_run = PrintRun.objects. \
                    filter(print_run_id = print_run_id) . \
                    values('print_run_id',
                           'edition_id',
                           'cover_id',
                           'print',
                           'cover_price',
                           cover_filename=F('cover__cover_filename'),
                           cover_filepath=F('cover__artwork__artist__cover_filepath'),
                           author_name=F('cover__book__author__name'),
                           title=F('cover__book__title'),
                           ). \
                    order_by ('order')
        return print_run

    @staticmethod
    def panorama_list():
        panoramas = Panorama.objects. \
                    values('panorama_id',
                           'order',
                           'description',
                           cover_filename=F('filename'),
                           cover_filepath=F('artist__cover_filepath'),
                           author_name=F('author__name'),
                           artist_name=F('artist__name'),
                            ). \
                    order_by('order')
        return panoramas

    @staticmethod
    def panorama(pk=None):
        panorama = get_object_or_404(Panorama.objects.select_related('artist'), pk=pk)
        return panorama

    @staticmethod
    def print_run_ids():
        print_run_ids = PrintRun.objects.values('print_run_id').distinct()
        return print_run_ids

    @staticmethod
    def highest_print_run():
        print_run_id = PrintRun.objects.all().aggregate(Max('print_run_id'))
        return print_run_id

    @staticmethod
    def artbook(pk):
        artbook = get_object_or_404(Artbook.objects.select_related('artist'), pk=pk)
        return artbook

    @staticmethod
    def artbooks():
        # only select artbooks that have been indexed
        inner_queryset_artbook_list = ArtbookIndex.objects.values('artbook_id').distinct()
        artbooks = Artbook.objects.filter(artbook_id__in=inner_queryset_artbook_list)
        return artbooks

    @staticmethod
    def artbook_index(artbook_id):
        # adding book__author and book_author reduced num queries from 107 (Chiaroscuro) and 12ms to 2 queries and 1.34ms
        artbook_index = ArtbookIndex.objects.filter(artbook=artbook_id).order_by('page'). \
            select_related('artist', 'book', 'book__author', 'cover', 'book_author')

        return artbook_index

    @staticmethod
    def artbooks_index_artbooks():
        artbook_list = ArtbookIndex.objects \
            .order_by('book_author_name')
        return artbook_list