import pprint

from django.db.models import F
from django.db.models import Q
from django.db.models import Count

from bookcovers.models import Authors
from bookcovers.models import Artists
from bookcovers.models import ArtistAkas
from bookcovers.models import Artworks
from bookcovers.models import Books
from bookcovers.models import Covers
from bookcovers.models import Editions
from bookcovers.models import Countries

import math


class CoverQuerys:

    @staticmethod
    def artist_list():
        inner_queryset = Artworks.objects. \
            filter(theCover__flags__lt=256). \
            values_list('artwork_id', flat=True)

        artist_list = Artists.objects. \
            filter(theArtwork__in=inner_queryset). \
            values('artist_id', 'name'). \
            order_by('name'). \
            distinct()

        print(artist_list.query)
        print(artist_list.count())

        return artist_list

    @staticmethod
    def artist_cover_list(artist):
        """

        :param artist:
        :return:
        """
        print("artist is {}".format(artist.name))
        aka_inner_queryset = Artists.objects.filter(theArtist_aka__artist_aka_id=artist.pk)
        # print (aka_inner_queryset.query)
        # print (aka_inner_queryset)

        cover_list = Artworks.objects. \
            filter(Q(artist=artist) | Q(artist__in=aka_inner_queryset)). \
            filter(Q(theCover__flags__lt=256) & Q(theCover__is_variant=False) & Q(theCover__book=F('book'))). \
            values('theCover__cover_id',
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
        print(f"artist_cover_list.query is '{cover_list.query}'")
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

        # djabbic_v2
        # covers -> editions is one-to-one
        # can one-to-one field in model have related name and related query name?
        inner_queryset = Editions.objects \
            .filter(covers__flags__lt=256) \
            .values_list('edition_id', flat=True)
        # https://docs.djangoproject.com/en/2.0/ref/models/querysets/
        # flat=True returns a list of single items for a single field

        print(inner_queryset.query)
        print("count inner_queryset is", inner_queryset.count())
        print("len inner_queryset is", len(inner_queryset))
        print(inner_queryset)

        # https://docs.djangoproject.com/en/2.0/ref/models/querysets/#in
        # need to clean database

        author_list = Authors.objects \
            .filter(author_id=F('theBook__author')) \
            .filter(theBook__theEdition__edition_id__in=inner_queryset) \
            .values('author_id', 'name') \
            .order_by('name') \
            .distinct()


        print(author_list.query)
        print(author_list.count())

        return author_list

    @staticmethod
    def all_covers_of_all_books_for_author(author, all=True):
        """
        gets all covers of all books for this author
        :param author: author object to fetch covers for
        :param all: True = return all covers for all books
                    False = eliminates duplicate cover entries, where the same file is used for multiple cover records
        :return: dict queryset to fetch all covers of all books for this author
        """
        print("author is {}".format(author.name))
        aka_inner_queryset = Authors.objects.filter(theAuthor_aka__author_aka_id=author.pk)

        # this returns all covers for all books
        all_cover_list = Books.objects \
            .filter(Q(author=author) | Q(author__in=aka_inner_queryset)) \
            .filter(Q(theCover__flags__lt=256)) \
            .values('book_id',
                   'theCover__artwork__artist__cover_filepath',
                   'theCover__cover_filename',
                   'title',
                   'copyright_year',
                   'theCover__artwork__year') \
            .order_by('copyright_year',
                      'book_id',
                      'theCover__artwork__year')

        # .filter(Q(theCover__flags__lt=256) & Q(pk=F('theCover__book'))) \

        # this eliminates duplicate cover entries, where the same file is used for multiple cover records
        # eg John Wyndham, The Chrysalids, by Brian Cronin covers: 645, 646
        dedup_cover_list = Books.objects \
            .filter(Q(author=author) | Q(author__in=aka_inner_queryset)) \
            .filter(Q(theCover__flags__lt=256)) \
            .values('book_id',
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
            print (f"author {author.name}: has unknown cover")
            author_directory = author.name.replace(" ", "").replace(".","")
            for cover in cover_list:
                if cover['theCover__artwork__artist__cover_filepath'] == "BookCovers/Images/Unknown/":
                    cover['theCover__artwork__artist__cover_filepath'] = f"BookCovers/Images/Unknown/{author_directory}/"
        else:
            print (f"author {author.name}: has no unknown covers")

        #print (cover_list)
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

        inner_queryset = Books.objects.filter(Q(book_id=book.book_id)).values_list('theEdition__edition_id', flat=True)

        # pk is book_id
        title_cover_list = Covers.objects \
            .filter(book=book, flags__lt=256) \
            .filter(edition__in=inner_queryset) \
            .values('artwork__artist__cover_filepath',
                    'cover_filename',
                    'edition__country',
                    'edition__country__display_order',
                    'edition__print_year') \
            .order_by('edition__country__display_order','edition__print_year')

        return title_cover_list

    @staticmethod
    def book_list():
        book_list = Books.objects.filter(theCover__flags__lt=256).values('book_id')

        return book_list

