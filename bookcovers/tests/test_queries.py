import itertools

from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import F
from django.db.models import Q

from bookcovers.models import Artists
from bookcovers.models import Author
from bookcovers.models import Books
from bookcovers.models import Covers
from bookcovers.models import Artworks

from bookcovers.original_raw_querys import OriginalRawQuerys
from bookcovers.cover_querys import CoverQuerys



# Using the unittest framework to test the django queries against the original raw sql queries

class QueryTestCase(TestCase):

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

class SubjectQueryTest(QueryTestCase):
    """
        subject may be Artists, Authors, Books

    """

    #  refactor to take key dicts and move to QueryTestCase
    def subject_matches(self, subject_pk, expected_subject, actual_subject):
        # keys in dictionary returned from raw sql query
        expected_keys = [subject_pk, "name"]
        # keys in dictionary returned from django query
        actual_keys = [subject_pk, "name"]
        self.record_matches(expected_subject, expected_keys, actual_subject, actual_keys)

    def print_cover_lists(self, raw_cover_list, cover_list):
        for raw_cover in raw_cover_list:
            print(f"raw book_id is {raw_cover['book_id']}")
        for cover in cover_list:
            cover_dict = "".join(str(key) + ':' + str(value) + ', ' for key, value in cover.items())
            print(cover_dict)


class CoverListQueryTest(SubjectQueryTest):
    """
    Tests lists of covers for an individual artist, author, or book
    """

    def __init__(self, list_query, model, item_desc, primary_key, raw_cover_query, django_cover_query, expected_keys, actual_keys):
        super().__init__()
        self.item_list_query = list_query
        self.model = model
        self.item_desc = item_desc
        self.primary_key = primary_key
        self.raw_cover_query = raw_cover_query
        self.django_cover_query = django_cover_query

        self.expected_keys = expected_keys
        self.actual_keys = actual_keys

    def validate_all_lists_of_covers(self):
        """
        Loops through all artists, authors, or books from list_query and
        validates the cover (or book) list for each entry in the list

        :param list_query:  query to create list of artists or authors
        :param model:       model instance, eg Author or Artist
        :param subject:     author, artist, or book
        :param primary_key: name of primary key
        :param raw_cover_query:  original raw query to generate list of covers
        :return:
        """
        print("===========================================")
        print(f"Test List of Covers for each {self.item_desc}")
        print("===========================================")

        list = self.item_list_query()
        for item in list:
            id = item[self.primary_key]
            print(f"{self.item_desc} id:{id}")
            the_item = get_object_or_404(self.model, pk=id)
            self.cover_list_matches(subject=the_item)

        print(f"num {self.item_desc}s is {len(list)}")

    def cover_list_matches(self, subject):
        """
        Tests lists of covers for an individual artist, author, or book

        :param item:     author, artist, or book model instance
        :param original_raw_query:
        :return:
        """
        raw_cover_list = self.raw_cover_query(subject.pk, return_dict=True)
        expected_num_covers = len(raw_cover_list)

        cover_list = self.django_cover_query(subject)
        num_covers = len(cover_list)

        print(f"expected_num_covers is {expected_num_covers}, num_covers is {num_covers}")

        self.print_cover_lists(raw_cover_list, cover_list)
        try:
            self.assertEqual(expected_num_covers, num_covers)
        except AssertionError as e:
            print("==============Expected (original raw)================")
            print(f"Original query is\n{raw_cover_list.query}\n")
            print(f"Original {self.item_desc} cover list is\n{raw_cover_list}\n")
            print("=========================Actual=====================")
            print(f"{self.item_desc} cover_list query is:\n{cover_list.query}")
            print(f"{self.item_desc} cover_list is:\n {cover_list}")
            print("====================================================")
            raise

        #  for each cover: check expected cover data matches actual cover data
        for raw_cover, cover in zip(raw_cover_list, cover_list):
            if self.item_desc == "author":
                if raw_cover['cover_filepath'] == "BookCovers/Images/Unknown/":
                    try:
                        real_author = Author.objects.get(Q(theAuthor_aka__real_name=1) & (
                                Q(theAuthor_aka__author_aka_id=subject.pk) | Q(theAuthor_aka__author_id=subject.pk)))
                    except Author.DoesNotExist as e:
                        real_author = subject

                    print(f"real author name is '{real_author.name}'")
                    author_directory = real_author.name.replace(" ", "").replace(".", "")
                    raw_cover['cover_filepath'] = f"BookCovers/Images/Unknown/{author_directory}/"

            self.record_matches(raw_cover, self.expected_keys, cover, self.actual_keys)


# python manage.py test bookcovers.tests.test_queries.AuthorQueryTests --settings=djabbic.testsettings
class AuthorQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'AuthorAkas.json',
                'Countries.json',
                'Sets.json',
                'Series.json',
                'BooksSeries.json',
                'SetExceptions.json',]

    def setUp(self):
        self.author_list_query = CoverQuerys.author_list

    def test_author_name(self):
        author = Author.objects.get(pk=6)
        expected_author_name = "Philip K. Dick"
        self.assertEqual(expected_author_name, author.name)

    # =====================================================
    # Test list of authors
    # =====================================================
    def test_aauthor_list(self):
        """ test author list """
        raw_author_list = OriginalRawQuerys.author_list(True)
        expected_num_authors = len(raw_author_list)

        author_list = self.author_list_query()
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
        test list of all covers for each author in db
        """
        cover_list_test = CoverListQueryTest(list_query=self.author_list_query,
                                             model=Author,
                                             item_desc="author",
                                             primary_key="author_id",
                                             raw_cover_query=OriginalRawQuerys.author_cover_list,
                                             django_cover_query=CoverQuerys.all_covers_of_all_books_for_author,
                                             expected_keys=["book_id", "cover_filepath", "cover_filename",
                                                            "copyright_year"],
                                             actual_keys=["book_id", "theCover__artwork__artist__cover_filepath",
                                                          "theCover__cover_filename",
                                                          "copyright_year"]
                                             )

        cover_list_test.validate_all_lists_of_covers()

    def test_authors_book_list(self):
        """
        test list of books for each author in db
        """
        cover_list_test = CoverListQueryTest(list_query=self.author_list_query,
                                             model=Author,
                                             item_desc="author",
                                             primary_key="author_id",
                                             raw_cover_query=OriginalRawQuerys.author_book_list,
                                             django_cover_query=CoverQuerys.books_for_author,
                                             expected_keys=["book_id", "copyright_year"],
                                             actual_keys=["book_id", "copyright_year"]
                                             )

        cover_list_test.validate_all_lists_of_covers()

    def test_an_author_book_list(self):
        """
        test list of books for given author
        """
        author_id =11
        author = get_object_or_404(Author, pk=author_id)

        cover_list_test = CoverListQueryTest(list_query=self.author_list_query,
                                             model=Author,
                                             item_desc="author",
                                             primary_key="author_id",
                                             raw_cover_query=OriginalRawQuerys.author_book_list,
                                             django_cover_query=CoverQuerys.books_for_author,
                                             expected_keys=["book_id", "copyright_year"],
                                             actual_keys=["book_id", "copyright_year"]
                                             )
        cover_list_test.cover_list_matches(author)

    def test_author_sets_list(self):
        print ("===========================================")
        print (f"Test List of Sets for each author")
        print ("===========================================")

        author_list = self.author_list_query()
        for author in author_list:
            author_id = author["author_id"]
            self.check_author_set_list(author_id)

        print (f"num authors is {len(author_list)}")

    def check_author_set_list(self, author_id):
        # return set list as dictionary
        raw_set_list = OriginalRawQuerys.author_set_list(author_id, return_dict=True)
        expected_num_sets = len(raw_set_list)

        author_set_list = CoverQuerys.author_set_list(author_id)
        #print(f"author {author_id}, set list {author_set_list}")
        actual_num_sets = len(author_set_list)

        self.assertEqual(expected_num_sets, actual_num_sets)

        if expected_num_sets > 0:
            print("=============================================")
            print(f"Test {expected_num_sets} sets for author {author_id}")
            print(f"author {author_id}, set list {author_set_list}")
            print("==============================================")

            expected_keys = ["set_id", "series_id", "author_id", "artist_id", "imprint_id", "description", "panorama_id"]

            #  for each set: check expected data matches actual data
            for raw_set, set in zip(raw_set_list, author_set_list):
                self.record_matches(raw_set, expected_keys, set, expected_keys)

                # check set cover list
                print (f"artist: {set['artist_id']}")
                self.check_author_artist_covers_list(author=author_id, artist=set['artist_id'])

    def check_author_artist_covers_list(self, author=None, artist=None):
        print ("==============================================")
        print (f"Test Set Covers for author {author} and artist {artist}")
        print ("==============================================")

        # return original cover list as dictionary
        original_cover_list = OriginalRawQuerys.author_artist_set_cover_list(author, artist, return_dict=True)
        expected_num_covers = len(original_cover_list)
        print(f"expected number of covers is {expected_num_covers}")
        print(f"original_cover_list is {original_cover_list}")

        set_cover_list = CoverQuerys.author_artist_set_cover_list(author=author, artist=artist)
        actual_num_covers = len(set_cover_list)
        print(f"actual number of covers is {actual_num_covers}")
        print(f"set_cover_list is {set_cover_list}")

        self.assertEqual(expected_num_covers, actual_num_covers, msg=f"author={author}, artist={artist}")

        # keys in dictionary returned from raw sql query
        expected_keys = ["cover_filepath", "cover_id", "cover_filename", "artwork_id"]
        # keys in dictionary returned from django query
        actual_keys = ['artwork__artist__cover_filepath', 'cover_id', 'cover_filename', 'artwork_id']

        #  for each cover: check expected cover data matches actual cover data
        for raw_cover, cover in zip(original_cover_list, set_cover_list):
            self.record_matches(raw_cover, expected_keys, cover, actual_keys)


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
        self.artist_list_query = CoverQuerys.artist_list


    def test_artist_name(self):
        artist = Artists.objects.get(pk=83)
        expected_artist_name = "Anthony Roberts"
        self.assertEqual(expected_artist_name, artist.name)

    # test artist list
    # tests are run in alphabetic order
    # tests are independent but I want this one to run first
    def test_aartist_list(self):
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
        cover_list_test = CoverListQueryTest(list_query=self.artist_list_query,
                                             model=Artists,
                                             item_desc="artist",
                                             primary_key="artist_id",
                                             raw_cover_query=OriginalRawQuerys.artist_cover_list,
                                             django_cover_query=CoverQuerys.artist_cover_list,
                                             expected_keys=["book_id", "cover_filename", "artwork_id", "year"],
                                             actual_keys=["book", "theCover__cover_filename", "artwork_id", "year"]
                                             )

        cover_list_test.validate_all_lists_of_covers()


class BookQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json']

    def setUp(self):
        self.book_list_query = CoverQuerys.book_list

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
            try:
                self.assertEqual(expected_value, actual_value)
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
        cover_list_test = CoverListQueryTest(list_query=self.book_list_query,
                                             model=Books,
                                             item_desc="book",
                                             primary_key="book_id",
                                             raw_cover_query=OriginalRawQuerys.author_covers_for_title,
                                             django_cover_query=CoverQuerys.all_covers_for_title,
                                             expected_keys=["cover_filepath", "cover_filename", "print_year",
                                                            "country_id", "display_order"],
                                             actual_keys=["artwork__artist__cover_filepath", "cover_filename",
                                                          "edition__print_year",
                                                          "edition__country", "edition__country__display_order"]
                                             )

        cover_list_test.validate_all_lists_of_covers()

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
        self.validate_list_of_covers_for_all_books()

    def validate_list_of_covers_for_all_books(self):
        print ("==============================================")
        print (f"Test List of Covers for artwork for each book")
        print ("==============================================")

        book_list = CoverQuerys.book_list()
        for the_book in book_list:
            book_id = the_book['book_id']
            print("==============================================")
            print (f"ArtworkQueryTests: book is {book_id}")
            print("==============================================")
            self.validate_list_of_covers_for_book(book_id)

        print (f"num books is {len(book_list)}")

    def validate_list_of_covers_for_book(self, book_id):
        the_book = get_object_or_404(Books, pk=book_id)
        # test covers per artist that did a cover for this book
        artist_list = Artists.objects.filter(theArtwork__book__pk=book_id)
        print (f"the_book is '{the_book}' artist_list is '{artist_list}''")
        for artist in artist_list:
            # we now have a book id and an artist id from which we can get the artwork id
            try:
                artwork = get_object_or_404(Artworks, book_id=book_id, artist_id=artist.pk)
                print("==============================================")
                print(f"artwork is'{artwork}")
                print("==============================================")
                self.artwork_cover_list_matches(the_book, artist, artwork, self.original_raw_query)
            except Artworks.MultipleObjectsReturned:
                # There is at least one instance in which the artist has created different covers for the same book
                # Bruce Pennington, Decision at Doona
                artwork_list = Artworks.objects.filter(book_id=book_id, artist_id=artist.pk)
                # yes, this means we will test it twice
                for artwork in artwork_list:
                    print("==============================================")
                    print(f"artwork is'{artwork}")
                    print("==============================================")
                    self.artwork_cover_list_matches(the_book, artist, artwork, self.original_raw_query)

    def artwork_cover_list_matches(self, book, artist, artwork, original_raw_query):
        raw_cover_list = self.artwork_original_query(book, artwork, original_raw_query)
        expected_num_covers = len(raw_cover_list)

        artwork_cover_list = CoverQuerys.all_covers_for_artwork(artwork)
        num_covers = len(artwork_cover_list)

        print(f"expected_num_covers is {expected_num_covers}, num_covers is {num_covers}")

        self.print_cover_lists(raw_cover_list, artwork_cover_list)

        try:
            self.assertEqual(expected_num_covers, num_covers)
        except AssertionError as e:
            print("==============Expected (original raw)================")
            #print(f"Original query is\n{raw_cover_list.query}\n")
            print(f"Original {self.subject_name} cover list is\n{raw_cover_list}\n")
            print("=========================Actual=====================")
            print(f"{self.subject_name} cover_list query is:\n{artwork_cover_list.query}")
            print(f"{self.subject_name} cover_list is:\n {artwork_cover_list}")
            print("====================================================")
            raise

        #  for each cover: check expected cover data matches actual cover data
        for raw_cover, cover in zip(raw_cover_list, artwork_cover_list):
            self.record_matches(raw_cover, self.expected_keys, cover, self.actual_keys)

    def artwork_original_query(self, book, artwork, original_raw_query):
        print(f"ArtworkQueryTests: book.pk is {book.pk} artwork.artist.pk is {artwork.artist.pk}")
        raw_cover_list = original_raw_query(book.pk, artwork.artist.pk, return_dict=True)
        return raw_cover_list

# python manage.py test bookcovers.tests.test_queries.AdhocQueryTests --settings=djabbic.testsettings
class AdhocQueryTests(QueryTestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',
                'Sets.json',
                'Series.json',
                'BooksSeries.json',
                'SetExceptions.json',]

    def test_sets(self):
        author_id = 15

        print("==============================================")
        print(f"Test Set Covers for author {author_id}")
        print("==============================================")
        expected_num_covers = 18

        all_list = CoverQuerys.set_covers_by_artist(author=author_id)
        num_covers = len(all_list)

        # use list to avoid remaining elements truncated
        # otherwise repr is used to represent queryset
        print(f"covers {list(all_list)}")

        self.assertEqual(expected_num_covers, num_covers)


    def test_author_set_list(self):
        author_id = 15
        print ("==============================================")
        print (f"Test Sets for author {author_id}")
        print ("==============================================")
        set_query=f"SELECT sets.*, authors.name FROM sets, authors " \
                  f"WHERE sets.author_id = {author_id} AND sets.author_id = authors.author_id"

        # return set list as dictionary
        original_set_list = OriginalRawQuerys.adhoc_query(set_query, return_dict=True)
        print(f"number of sets is {len(original_set_list)}")
        print(f"original_set_list is {original_set_list}")

        author_set_list = CoverQuerys.author_set_list(author_id)
        print(f"number of sets is {len(author_set_list)}")
        print(f"author_set_list is {author_set_list}")


    def test_author_books(self):
        author_id = 5
        print ("==============================================")
        print (f"Test List of Books for author {author_id}")
        print ("==============================================")
        author = get_object_or_404(Author, pk=author_id)
        book_list = CoverQuerys.books_for_author(author)
        print(f"number of books is {len(book_list)}")
        print(f"book_list is {book_list}")

        for book in book_list:
            print (f"book is '{book}'")

