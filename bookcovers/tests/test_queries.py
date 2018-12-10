import itertools

from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.conf import settings

from bookcovers.models import Artists
from bookcovers.models import Authors
from bookcovers.models import Books
from bookcovers.models import Covers
from bookcovers.models import Artworks

from bookcovers.original_raw_querys import OriginalRawQuerys
from bookcovers.cover_querys import CoverQuerys



# Using the unittest framework to test the django queries against the original raw sql queries

class SubjectQueryTest(TestCase):
    """
        subject: subject model: Artists, Authors, Books
        pk_name: name of private key field for subject
        subject_query: CoverQuerys.<subject>_list, method returning query to list all subjects
        original_raw_query: OriginalRawQuerys.<subject>_cover_list

    """

    def subject_matches(self, subject_pk, expected_subject, actual_subject):
        # keys in dictionary returned from raw sql query
        expected_keys = [subject_pk, "name"]
        # keys in dictionary returned from django query
        actual_keys = [subject_pk, "name"]
        self.record_matches(expected_subject, expected_keys, actual_subject, actual_keys)

    def record_matches(self, expected_record, expected_keys, actual_record, actual_keys):
        # https://docs.python.org/3/library/functions.html#zip
        for expected_key, actual_key in zip(expected_keys, actual_keys):
            expected_value = expected_record[expected_key]
            actual_value = actual_record[actual_key]
            #print(f"expected_value is '{expected_value}', actual_value is '{actual_value}'")
            try: self.assertEqual(expected_value, actual_value)
            except AssertionError as e:
                print ("================================================================================")
                print (f"Expected: {expected_record}")
                print (f"Actual: {actual_record}")
                print ("================================================================================")
                raise

    def print_cover_lists(self, raw_cover_list, cover_list):
        for raw_cover in raw_cover_list:
            print(f"raw book_id is {raw_cover['book_id']}")
        for cover in cover_list:
            cover_dict = "".join(str(key) + ':' + str(value) + ', ' for key, value in cover.items())
            print(cover_dict)

    def validate_list_of_covers_for_subject(self):
        print ("===========================================")
        print (f"Test List of Covers for each {self.subject_name}")
        print ("===========================================")

        subject_list = self.subject_query()
        for subject in subject_list:
            subject_id = subject[self.pk_name]
            print (f"subject:{self.subject_name} id:{subject_id}")
            the_subject = get_object_or_404(self.subject_model, pk=subject_id)
            self.subject_cover_list_matches(the_subject, self.original_raw_query)

        print (f"num {self.subject_name}s is {len(subject_list)}")

    def subject_cover_list_matches(self, subject, original_raw_query):
        raw_cover_list = self.subject_original_query(subject, original_raw_query)
        expected_num_covers = len(raw_cover_list)

        subject_cover_list = self.all_covers_for_subject(subject)
        num_covers = len(subject_cover_list)

        print(f"expected_num_covers is {expected_num_covers}, num_covers is {num_covers}")

        self.print_cover_lists(raw_cover_list, subject_cover_list)
        try: self.assertEqual(expected_num_covers, num_covers)
        except AssertionError as e:
            print ("==============Expected (original raw)================")
            print (f"Original query is\n{self.raw_cover_list.query}\n")
            print (f"Original {self.subject_name} cover list is\n{self.subject_cover_list}\n")
            print ("=========================Actual=====================")
            print (f"{self.subject_name} cover_list query is:\n{cover_list.query}")
            print (f"{self.subject_name} cover_list is:\n {cover_list}")
            print ("====================================================")
            raise

        #  for each cover: check expected cover data matches actual cover dat
        for raw_cover, cover in zip(raw_cover_list, subject_cover_list):
            if self.subject_name == "author":
                if raw_cover['cover_filepath'] == "BookCovers/Images/Unknown/":
                    author_directory = subject.name.replace(" ", "").replace(".", "")
                    raw_cover['cover_filepath'] = f"BookCovers/Images/Unknown/{author_directory}/"
            self.record_matches(raw_cover, self.expected_keys, cover, self.actual_keys)

    def subject_original_query(self, subject, original_raw_query):
        print(f"subject is {subject}")
        raw_cover_list = original_raw_query(subject.pk, return_dict=True)
        return raw_cover_list

class AuthorQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'AuthorAkas.json',
                'Countries.json']

    def setUp(self):
        self.subject_model = Authors
        self.subject_name = "author"
        self.pk_name = "author_id"
        self.subject_query = CoverQuerys.author_list
        self.original_raw_query = OriginalRawQuerys.author_cover_list
        self.all_covers_for_subject = CoverQuerys.all_covers_of_all_books_for_author
        # keys in dictionary returned from raw sql query
        self.expected_keys = ["book_id", "cover_filepath", "cover_filename", "copyright_year"]
        # keys in dictionary returned from django query
        self.actual_keys = ["book_id", "theCover__artwork__artist__cover_filepath", "theCover__cover_filename",
                       "copyright_year"]

    def test_author_name(self):
        author = Authors.objects.get(pk=6)
        expected_author_name = "Philip K. Dick"
        self.assertEqual(expected_author_name, author.name)

    # =====================================================
    # Test list of authors
    # =====================================================
    def test_author_alist(self):
        """ test author list """
        raw_author_list = OriginalRawQuerys.author_list(True)
        expected_num_authors = len(raw_author_list)

        author_list = CoverQuerys.author_list()
        # https: // docs.djangoproject.com / en / 2.1 / ref / models / querysets /
        # A QuerySet  is evaluated when you call len() on it.
        num_authors = len(author_list)

        print(f"expected_num_authors is {expected_num_authors}, num_authors is {num_authors}")
        try:
            self.assertEqual(expected_num_authors, num_authors)
        except AssertionError as e:
            print(f"raw_author_list is\n{raw_author_list}")
            print(f"authorlist is\n{author_list}")
            raise

        # for each author: compare expected name against actual name
        for raw_author_list, author_list in zip(raw_author_list, author_list):
            self.subject_matches("author_id", raw_author_list, author_list)

    def test_authors_cover_list(self):
        """
        test list of book covers for each author in db
        """
        self.validate_list_of_covers_for_subject()


class ArtistQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'ArtistAkas.json',
                'Countries.json']

    def setUp(self):
        self.subject_model = Artists
        self.subject_name = "artist"
        self.pk_name = "artist_id"
        self.subject_query = CoverQuerys.artist_list
        self.original_raw_query = OriginalRawQuerys.artist_cover_list
        self.all_covers_for_subject = CoverQuerys.artist_cover_list
        # keys in dictionary returned from raw sql query
        self.expected_keys = ["book_id", "cover_filename", "artwork_id", "year"]
        # keys in dictionary returned from django query
        self.actual_keys = ["book", "theCover__cover_filename", "artwork_id", "year"]

    def test_artist_name(self):
        artist = Artists.objects.get(pk=83)
        expected_artist_name = "Anthony Roberts"
        self.assertEqual(expected_artist_name, artist.name)

    # test artist list
    # tests are run in alphabetic order
    # tests are independent but I want this one to run first
    def test_artist_alist(self):
        raw_artist_list = OriginalRawQuerys.artist_list(True)
        expected_num_artists = len(raw_artist_list)

        artist_list = CoverQuerys.artist_list()
        # https: // docs.djangoproject.com / en / 2.1 / ref / models / querysets /
        # A QuerySet  is evaluated when you call len() on it.
        num_artists = len(artist_list)

        print (f"expected_num_artists is {expected_num_artists}, num_artists is {num_artists}")
        try: self.assertEqual(expected_num_artists, num_artists)
        except AssertionError as e:
            print (f"raw_artist_list is\n{raw_artist_list}")
            print (f"artist_list is\n{artist_list}")
            raise

        # for each artist: compare expected name against actual  name
        for raw_artist_list, artist_list in zip(raw_artist_list, artist_list):
            self.subject_matches("artist_id", raw_artist_list, artist_list)

    def test_artists_cover_list(self):
        """
        test list of book covers for each artist in db
        """
        self.validate_list_of_covers_for_subject()


class BookQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json']

    def setUp(self):
        self.subject_model = Books
        self.subject_name = "book"
        self.pk_name = "book_id"
        self.subject_query = CoverQuerys.book_list
        self.original_raw_query = OriginalRawQuerys.author_covers_for_title
        self.all_covers_for_subject = CoverQuerys.all_covers_for_title
        # keys in dictionary returned from raw sql query
        self.expected_keys = ["cover_filepath", "cover_filename", "print_year", "country_id", "display_order"]
        # keys in dictionary returned from django query
        self.actual_keys = ["artwork__artist__cover_filepath", "cover_filename", "edition__print_year",
                            "edition__country", "edition__country__display_order"]


    def test_book_list(self):
        book_query="select books.book_id, covers.flags from books, covers " \
                   "where books.book_id = covers.book_id and covers.flags < 256 order by books.book_id;"
        # return book list as dictionary
        raw_book_list = OriginalRawQuerys.adhoc_query(book_query, True)
        expected_num_books = len(raw_book_list)
        print (f"raw_book_list is {raw_book_list[:20]}")

        book_list = CoverQuerys.book_list()
        print (f"expected number of books is {expected_num_books}, number of books is {len(book_list)}")
        print (f"book_list is {book_list}")

        for expected, actual in zip(raw_book_list, book_list):
            expected_value = expected['book_id']
            actual_value = actual['book_id']
            #print(f"expected '{expected}', actual '{actual}'")
            try: self.assertEqual(expected_value, actual_value)
            except AssertionError as e:
                print ("================================================================================")
                print (f"Expected: {expected}")
                print (f"Actual: {actual}")
                print ("================================================================================")
                raise


    def test_books_cover_list(self):
        """
        test list of covers for each book title in db
        """
        self.validate_list_of_covers_for_subject()

class ArtworkQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json']

    def setUp(self):
        self.subject_model = Artworks
        self.subject_name = "artwork"
        self.pk_name = "artwork_id"
        self.subject_query = CoverQuerys.book_list
        self.original_raw_query = OriginalRawQuerys.artwork_cover_list
        self.all_covers_for_subject = CoverQuerys.all_covers_for_artwork
        # keys in dictionary returned from raw sql query
        self.expected_keys = ["cover_filepath", "cover_filename", "cover_id", "book_id", "edition_id", "artist_id", "artwork_id"]
        # keys in dictionary returned from django query
        self.actual_keys = ["artwork__artist__cover_filepath", "cover_filename", "cover_id",
                            "book__pk", "edition__pk", "artwork__artist__pk", "artwork__pk"]

    def test_artworks_cover_list(self):
        """
        test list of covers for each book title in db
        """
        self.validate_list_of_covers_for_book()

        #the_book = get_object_or_404(Books, pk=16)
        #print (f"the_book is {the_book}")
        #self.subject_original_query(the_book, self.original_raw_query)

    def validate_list_of_covers_for_book(self):

        print ("==============================================")
        print (f"Test List of Covers for artwork for each book")
        print ("==============================================")

        book_list = CoverQuerys.book_list()
        for the_book in book_list:
            book_id = the_book['book_id']
            print (f"ArtworkQueryTests: book_id is {book_id}")
            the_book = get_object_or_404(Books, pk=book_id)
            print (f"ArtworkQueryTests: the_book is {the_book}")
            cover_list = Covers.objects.filter(book__pk=book_id)
            for the_cover in cover_list:
                the_artwork = get_object_or_404(Artworks, pk=the_cover.artwork.pk)
                print (f"the_artwork is {the_artwork}")
                # up to here
                # python manage.py test bookcovers.tests.test_queries.ArtworkQueryTests --settings=djabbic.testsettings
                # ArtworkQueryTests: book_id is 82
                # ArtworkQueryTests: the_book is Decision at Doona
                # the_artwork is Bruce Pennington, Decision At Doona, 1981
                # AssertionError: 2 != 1
                self.artwork_cover_list_matches(the_book, the_artwork, self.original_raw_query)

        print (f"num books is {len(book_list)}")

    def artwork_cover_list_matches(self, book, artwork, original_raw_query):
        raw_cover_list = self.artwork_original_query(book, artwork, original_raw_query)
        expected_num_covers = len(raw_cover_list)

        subject_cover_list = self.all_covers_for_subject(artwork)
        num_covers = len(subject_cover_list)

        print(f"expected_num_covers is {expected_num_covers}, num_covers is {num_covers}")

        self.print_cover_lists(raw_cover_list, subject_cover_list)
        try:
            self.assertEqual(expected_num_covers, num_covers)
        except AssertionError as e:
            print("==============Expected (original raw)================")
            print(f"Original query is\n{self.raw_cover_list.query}\n")
            print(f"Original {self.subject_name} cover list is\n{self.subject_cover_list}\n")
            print("=========================Actual=====================")
            print(f"{self.subject_name} cover_list query is:\n{cover_list.query}")
            print(f"{self.subject_name} cover_list is:\n {cover_list}")
            print("====================================================")
            raise

        #  for each cover: check expected cover data matches actual cover data
        for raw_cover, cover in zip(raw_cover_list, subject_cover_list):
            self.record_matches(raw_cover, self.expected_keys, cover, self.actual_keys)

    def artwork_original_query(self, book, artwork, original_raw_query):
        print(f"ArtworkQueryTests: book.pk is {book.pk} artwork.artist.pk is {artwork.artist.pk}")
        raw_cover_list = original_raw_query(book.pk, artwork.artist.pk, return_dict=True)
        return raw_cover_list
