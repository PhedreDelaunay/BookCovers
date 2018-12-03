import itertools

from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.conf import settings

from bookcovers.models import Artists
from bookcovers.models import Authors
from bookcovers.models import Books

from bookcovers.original_raw_querys import OriginalRawQuerys
from bookcovers.cover_querys import CoverQuerys



# Using the unittest framework to test the django queries against the original raw sql queries

class SubjectQueryTest(TestCase):

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

    # DRY
    # subjects: artist, author, book
    # test_subject_list
    #
    # test_list_of_covers_for_subjet
    #   get list of subject items
    # subject
    #   get record for subject
    # subject_cover_list_matches
    #   get list of covers for subject
    # cover_record_matches
    #   set expected and actual keys for cover data
    #   compare records

class AuthorQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'AuthorAkas.json',
                'Countries.json']

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

    # =====================================================
    # Test list of book covers for each author in db
    # =====================================================

    def test_authors_cover_list(self):
        author_list = CoverQuerys.author_list()

        for author in author_list:
            author_id = author['author_id']
            print (f"author_id is {author_id}")
            self.author_cover(author_id)

    def author_cover(self, author_id=None):
        """
        Test cover list for given author
        :param author_id:
        :return:
        """
        the_author = get_object_or_404(Authors, pk=author_id)
        self.author_cover_list_matches(the_author)

    # test author cover list
    def author_cover_list_matches(self, author):
        # return cover list as dictionary
        raw_cover_list = OriginalRawQuerys.author_cover_list(author_id=author.pk, return_dict=True)
        expected_num_covers = len(raw_cover_list)

        #print(f"cover_filepath is {artist.cover_filepath}")
        cover_list = CoverQuerys.all_covers_of_all_books_for_author(author, all=True)
        num_covers = len(cover_list)

        print (f"expected_num_covers is {expected_num_covers}, num_covers is {num_covers}")

        self.print_cover_lists(raw_cover_list, cover_list)
        try: self.assertEqual(expected_num_covers, num_covers)
        except AssertionError as e:
            print ("==============Expected (original raw)================")
            print (f"Original query is\n{raw_cover_list.query}\n")
            print (f"Original author cover list is\n{raw_cover_list}\n")
            print ("=========================Actual=====================")
            print (f"author cover_list query is:\n{cover_list.query}")
            print (f"author cover_list is:\n {cover_list}")
            print ("====================================================")
            raise

        #  for each cover: check expected cover data matches actual cover dat
        for raw_cover, cover in zip(raw_cover_list, cover_list):
            if raw_cover['cover_filepath'] == "BookCovers/Images/Unknown/":
                author_directory = author.name.replace(" ", "").replace(".", "")
                raw_cover['cover_filepath'] = f"BookCovers/Images/Unknown/{author_directory}/"
            self.cover_matches(raw_cover, cover)

    def cover_matches(self, expected_cover, actual_cover):
        # keys in dictionary returned from raw sql query
        expected_keys = ["book_id", "cover_filepath", "cover_filename", "copyright_year"]
        # keys in dictionary returned from django query
        actual_keys = ["book_id", "theCover__artwork__artist__cover_filepath", "theCover__cover_filename", "copyright_year"]
        # print (f"Expected: {expected_cover}")
        # print (f"Actual: {actual_cover}")
        self.record_matches(expected_cover, expected_keys, actual_cover, actual_keys)

    # def test_author_cover(self):
    #     self.author_cover(6)

    # move this to BookQueryTest
    # =====================================================
    # Test list of covers for each book in db
    # =====================================================
    def test_title_cover_list(self):
        print ("===========================================")
        print ("Test List of Covers for a Book Title")
        print ("===========================================")

        title_list = CoverQuerys.book_list()

        for book in title_list:
            book_id = book['book_id']
            self.title_cover(book_id)

    def title_cover(self, book_id=None):
        """
        Test cover list for given book title
        :param author_id:
        :return:
        """
        the_book = get_object_or_404(Books, pk=book_id)
        print(f"book_id is {book_id}, book is '{the_book.title}'")
        self.title_cover_list_matches(the_book)

    def title_cover_list_matches(self, book):
        """
        test list of all covers for the book title
        :return:
        """

        raw_title_cover_list =  OriginalRawQuerys.author_covers_for_title(book_id=book.pk, return_dict=True)
        expected_num_covers = len(raw_title_cover_list)

        title_cover_list = CoverQuerys.all_covers_for_title(book)
        num_title_covers = len(title_cover_list)

        print(f"expected_num_covers is {expected_num_covers}, num_title_covers is {num_title_covers}")
        try:
            self.assertEqual(expected_num_covers, num_title_covers)
        except AssertionError as e:
            print ("==============Expected (original raw)================")
            print (f"Original query is\n{raw_title_cover_list.query}\n")
            print (f"Original title cover list is\n{raw_title_cover_list}\n")
            print ("=========================Actual=====================")
            print (f"title cover_list query is:\n{title_cover_list.query}")
            print (f"title cover_list is:\n {title_cover_list}")
            print ("====================================================")
            raise

        #  for each cover: check expected cover data matches actual cover data
        for raw_title_cover, title_cover in zip(raw_title_cover_list, title_cover_list):
            self.title_cover_matches(raw_title_cover, title_cover)

    def title_cover_matches(self, expected_cover, actual_cover):
        # keys in dictionary returned from raw sql query
        expected_keys = ["cover_filepath", "cover_filename", "print_year", "country_id", "display_order"]
        # keys in dictionary returned from django query
        actual_keys = ["artwork__artist__cover_filepath", "cover_filename", "edition__print_year", "edition__country", "edition__country__display_order"]
        # print (f"Expected: {expected_cover}")
        # print (f"Actual: {actual_cover}")
        self.record_matches(expected_cover, expected_keys, actual_cover, actual_keys)


class ArtistQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'ArtistAkas.json',
                'Countries.json']

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

    def cover_matches(self, expected_cover, actual_cover):
        # keys in dictionary returned from raw sql query
        expected_keys = ["book_id", "cover_filename", "year"]
        # keys in dictionary returned from django query
        actual_keys = ["book", "theCover__cover_filename", "year"]
        # print (f"Expected: {expected_cover}")
        # print (f"Actual: {actual_cover}")

        self.record_matches(expected_cover, expected_keys, actual_cover, actual_keys)

    def artist_cover_list_matches(self, artist):
        # return cover list as dictionary
        raw_cover_list = OriginalRawQuerys.artist_cover_list(artist.pk, True)
        expected_num_covers = len(raw_cover_list)

        print(f"cover_filepath is {artist.cover_filepath}")
        cover_list = CoverQuerys.artist_cover_list(artist)
        num_covers = len(cover_list)
        print (f"cover_list is:\n {cover_list}")

        print (f"expected_num_covers is {expected_num_covers}, num_covers is {num_covers}")

        self.print_cover_lists(raw_cover_list, cover_list)
        try: self.assertEqual(expected_num_covers, num_covers)
        except AssertionError as e:
            print (f"cover_list query is:\n{cover_list.query}")
            raise

        #  for each cover: check expected cover data matches actual cover data
        for raw_cover, cover in zip(raw_cover_list, cover_list):
            self.cover_matches(raw_cover, cover)

    def test_artist_cover_list(self):
        artist_list = CoverQuerys.artist_list()

        for artist in artist_list:
            artist_id = artist['artist_id']
            print (f"artist_id is {artist_id}")
            the_artist = get_object_or_404(Artists, pk=artist_id)
            self.artist_cover_list_matches(the_artist)


class BookQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json']

    def test_book_list(self):
        book_query="select books.book_id, covers.flags from books, covers " \
                   "where books.book_id = covers.book_id and covers.flags < 256;"
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
