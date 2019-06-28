
from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.db.models import Q

from bookcovers.models import Artist
from bookcovers.models import Author
from bookcovers.models import Book
from bookcovers.models import Artwork

from bookcovers.original_raw_querys import OriginalRawQuerys
from bookcovers.cover_querys import CoverQuerys
from bookcovers.query_cache import QueryCache

def print_dict_list(list_of_dicts):
    for dict in list_of_dicts:
        print(f"{dict}")

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

    def item_matches(self, primary_key, field_name, expected_subject, actual_subject):
        # keys in dictionary returned from raw sql query
        expected_keys = [primary_key, field_name]
        # keys in dictionary returned from django query
        actual_keys = [primary_key, field_name]
        self.record_matches(expected_subject, expected_keys, actual_subject, actual_keys)

    def print_cover_lists(self, raw_cover_list, cover_list):
        for raw_cover in raw_cover_list:
            print(f"raw author_id: {raw_cover['author_id']} , book_id: {raw_cover['book_id']}, cover_id: {raw_cover['cover_id']}, "
                  f"edition_id: {raw_cover['edition_id']}, artwork_id: {raw_cover['artwork_id']},")
        for cover in cover_list:
            print(f"cover author_id: {cover['author_id']} , book_id: {cover['book_id']}, cover_id: {cover['cover_id']}, "
                  f"edition_id: {cover['edition_id']}, artwork_id: {cover['artwork_id']},")
            # cover_dict = "".join(str(key) + ':' + str(value) + ', ' for key, value in cover.items())
            # print(cover_dict)

    def print_cover_lists_simple(self, raw_cover_list, cover_list):
        for raw_cover in raw_cover_list:
            print(f"raw book_id is {raw_cover['book_id']}")
        for cover in cover_list:
            cover_dict = "".join(str(key) + ':' + str(value) + ', ' for key, value in cover.items())
            print(cover_dict)

class CoverListQueryTest(QueryTestCase):
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

        self.print_cover_lists_simple(raw_cover_list, cover_list)
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
            #print (f"cover_list_matches: cover is '{cover}'")
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


class SetQueryTest(QueryTestCase):

    def check_author_artist_covers_list(self, author, artist):
        print ("==============================================")
        print (f"Test Set Covers for author {author} and artist {artist}")
        print ("==============================================")

        # return original cover list as dictionary
        original_cover_list = OriginalRawQuerys.author_artist_set_cover_list(author, artist, return_dict=True)
        expected_num_covers = len(original_cover_list)
        print(f"expected number of covers is {expected_num_covers}")
        print(f"original_cover_list is {original_cover_list}")

        set, set_cover_list = CoverQuerys.author_artist_set_cover_list(author_id=author, artist_id=artist)
        actual_num_covers = len(set_cover_list)
        print(f"actual number of covers is {actual_num_covers}")
        print(f"set_cover_list is {set_cover_list}")

        self.assertEqual(expected_num_covers, actual_num_covers, msg=f"author={author}, artist={artist}")

        # keys in dictionary returned from raw sql query
        expected_keys = ["cover_filepath", "cover_id", "cover_filename", "artwork_id", "edition_id"]
        # keys in dictionary returned from django query
        actual_keys = ['cover_filepath', 'cover_id', 'cover_filename', 'artwork_id', 'edition_id']

        #  for each cover: check expected cover data matches actual cover data
        for raw_cover, cover in zip(original_cover_list, set_cover_list):
            self.record_matches(raw_cover, expected_keys, cover, actual_keys)

# python manage.py test bookcovers.tests.test_queries.AuthorQueryTests --settings=djabbic.testsettings
class AuthorQueryTests(QueryTestCase):
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
            self.item_matches("author_id", "name", raw_author_list, author_list)

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

# python manage.py test bookcovers.tests.test_queries.AuthorSetQueryTests --settings=djabbic.testsettings
class AuthorSetQueryTests(SetQueryTest):
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

    def test_a_num_author_sets(self):
        author_list = self.author_list_query()
        for author in author_list:
            author_id = author["author_id"]
            raw_set_list = OriginalRawQuerys.author_set_list(author_id, return_dict=True)
            expected_num_sets = len(raw_set_list)

            author_set_list = CoverQuerys.author_set_list(author_id)
            actual_num_sets = len(author_set_list)

            if expected_num_sets != 0 or actual_num_sets != 0:
                print("==============================================")
                print(f"Test Num sets for author {author_id}, {author['name']}")
                print("==============================================")
                print(f"Expected: {expected_num_sets}, actual: {actual_num_sets}")

            try: self.assertEqual(expected_num_sets, actual_num_sets)
            except AssertionError as e:
                print("================================================================================")
                print(f"covers {author_set_list}")
                print("================================================================================")
                raise

    def test_b_total_num_covers_in_author_sets(self):
        author_list = self.author_list_query()
        for author in author_list:
            author_id = author["author_id"]

            original_cover_list = OriginalRawQuerys.author_set_cover_list(author_id, return_dict=True)
            expected_num_covers = len(original_cover_list)

            all_list = CoverQuerys.author_set_covers(author_id=author_id)
            num_covers = len(all_list)

            if expected_num_covers != 0 or num_covers != 0:
                print("==============================================")
                print(f"Test Total Covers in sets for author {author_id}, {author['name']}")
                print("==============================================")
                print(f"Expected: {expected_num_covers}, actual: {num_covers}")

            try: self.assertEqual(expected_num_covers, num_covers)
            except AssertionError as e:
                # use list to avoid remaining elements truncated
                # otherwise repr is used to represent queryset
                print("================================================================================")
                print(f"covers {list(all_list)}")
                print("================================================================================")
                raise

    def test_c_author_sets_covers(self):
        """tests all the covers in all the sets for this author"""
        author_list = self.author_list_query()
        for author in author_list:
            author_id = author["author_id"]

            raw_cover_list = OriginalRawQuerys.author_set_cover_list(author_id, return_dict=True)
            expected_num_covers = len(raw_cover_list)

            cover_list = CoverQuerys.author_set_covers(author_id=author_id)
            num_covers = len(cover_list)

            if expected_num_covers != 0 or num_covers != 0:
                print("==============================================")
                print(f"Test all Covers in all Sets for Author {author_id}, {author['name']}")
                print("==============================================")
                print(f"Expected: {expected_num_covers}, actual: {num_covers}")

            self.assertEqual(expected_num_covers, num_covers)
            #self.print_cover_lists(raw_cover_list, cover_list)

            # keys in dictionary returned from raw sql query
            expected_keys = ["cover_filepath", "cover_id", "book_id", "artwork_id", "edition_id", "cover_filename"]
            # keys in dictionary returned from django query
            actual_keys = ['cover_filepath', 'cover_id', 'book__pk', 'artwork_id', 'edition_id', 'cover_filename']

            #  for each cover: check expected cover data matches actual cover data
            for raw_cover, cover in zip(raw_cover_list, cover_list):
                self.record_matches(raw_cover, expected_keys, cover, actual_keys)

    def test_d_author_sets_list(self):
        print ("===========================================")
        print (f"Test List of Sets for each author")
        print ("===========================================")

        author_list = self.author_list_query()
        for author in author_list:
            author_id = author["author_id"]

            # return set list as dictionary
            raw_set_list = OriginalRawQuerys.author_set_list(author_id, return_dict=True)
            expected_num_sets = len(raw_set_list)

            author_set_list = CoverQuerys.author_set_list(author_id)
            # print(f"author {author_id}, set list {author_set_list}")
            actual_num_sets = len(author_set_list)

            self.assertEqual(expected_num_sets, actual_num_sets)

            if expected_num_sets > 0:
                print("=============================================")
                print(f"Test {expected_num_sets} sets for author {author_id}")
                print(f"author {author_id}, set list {author_set_list}")
                print("==============================================")

                expected_keys = ["set_id", "series_id", "author_id", "artist_id", "imprint_id", "description",
                                 "panorama_id"]

                #  for each set: check expected data matches actual data
                for raw_set, set in zip(raw_set_list, author_set_list):
                    self.record_matches(raw_set, expected_keys, set, expected_keys)
        print (f"num authors is {len(author_list)}")

    def test_e_author_sets_list_covers(self):
        print ("===========================================")
        print (f"Test Covers in each individual Set for each authoro")
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

            #  for each set: check cover data matches actual data
            for set in author_set_list:
                artist_id = set['artist_id']
                print (f"artist: {artist_id}")
                self.check_author_artist_covers_list(author=author_id, artist=artist_id)


class BookQueryTests(QueryTestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json']

    def setUp(self):
        self.book_list_query = CoverQuerys.book_list

        self.subject_model = Book
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
                                             model=Book,
                                             item_desc="book",
                                             primary_key="book_id",
                                             raw_cover_query=OriginalRawQuerys.author_covers_for_title,
                                             django_cover_query=CoverQuerys.all_covers_for_title,
                                             expected_keys=["cover_filepath", "cover_filename", "print_year",
                                                            "country_id", "display_order"],
                                             actual_keys=["cover_filepath", "cover_filename",
                                                          "edition__print_year",
                                                          "edition__country", "display_order"]
                                             )

        cover_list_test.validate_all_lists_of_covers()


class ArtistQueryTests(QueryTestCase):
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
        artist = Artist.objects.get(pk=83)
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
            self.item_matches("artist_id", "name", raw_artist_list, artist_list)

    def test_artists_cover_list(self):
        """
        test list of book covers for each artist in db
        """
        cover_list_test = CoverListQueryTest(list_query=self.artist_list_query,
                                             model=Artist,
                                             item_desc="artist",
                                             primary_key="artist_id",
                                             raw_cover_query=OriginalRawQuerys.artist_cover_list,
                                             django_cover_query=CoverQuerys.artist_cover_list,
                                             expected_keys=["book_id", "cover_filename", "artwork_id", "year"],
                                             actual_keys=["book", "theCover__cover_filename", "artwork_id", "year"]
                                             )

        cover_list_test.validate_all_lists_of_covers()


# python manage.py test bookcovers.tests.test_queries.AuthorSetQueryTests --settings=djabbic.testsettings
class ArtistSetQueryTests(SetQueryTest):
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
                'SetExceptions.json', ]

    def setUp(self):
        self.artist_list_query = CoverQuerys.artist_list

    def test_a_num_artist_sets(self):
        artist_list = self.artist_list_query()
        for artist in artist_list:
            artist_id = artist["artist_id"]
            raw_set_list = OriginalRawQuerys.artist_set_list(artist_id, return_dict=True)
            expected_num_sets = len(raw_set_list)

            artist_set_list = CoverQuerys.artist_set_list(artist_id)
            actual_num_sets = len(artist_set_list)

            if expected_num_sets != 0 or actual_num_sets != 0:
                print("==============================================")
                print(f"Test Num sets for artist {artist_id}, {artist['name']}")
                print("==============================================")
                print(f"Expected: {expected_num_sets}, actual: {actual_num_sets}")

            try:
                self.assertEqual(expected_num_sets, actual_num_sets)
            except AssertionError as e:
                print("================================================================================")
                print(f"covers {artist_set_list}")
                print("================================================================================")
                raise

    def test_b_total_num_covers_in_artist_sets(self):
        artist_list = self.artist_list_query()
        for artist in artist_list:
            artist_id = artist["artist_id"]

            original_cover_list = OriginalRawQuerys.artist_set_cover_list(artist_id, return_dict=True)
            expected_num_covers = len(original_cover_list)

            all_list = CoverQuerys.artist_set_covers(artist_id=artist_id)
            num_covers = len(all_list)

            if expected_num_covers != 0 or num_covers != 0:
                print("==============================================")
                print(f"Test Total Covers in sets for artist {artist_id}, {artist['name']}")
                print("==============================================")
                print(f"Expected: {expected_num_covers}, actual: {num_covers}")

            try: self.assertEqual(expected_num_covers, num_covers)
            except AssertionError as e:
                # use list to avoid remaining elements truncated
                # otherwise repr is used to represent queryset
                print("================================================================================")
                print(f"covers {list(all_list)}")
                print("================================================================================")
                raise

    def test_c_artist_sets_covers(self):
        """tests all the covers in all the sets for each artist"""
        artist_list = self.artist_list_query()
        for artist in artist_list:
            artist_id = artist["artist_id"]

            raw_cover_list = OriginalRawQuerys.artist_set_cover_list(artist_id, return_dict=True)
            expected_num_covers = len(raw_cover_list)

            cover_list = CoverQuerys.artist_set_covers(artist_id=artist_id)
            num_covers = len(cover_list)

            if expected_num_covers != 0 or num_covers != 0:
                #print (f"test_c: {raw_cover_list}")
                print("==============================================")
                print(f"Test all Covers in all Sets for Artist {artist_id}, {artist['name']}")
                print("==============================================")
                print(f"Expected: {expected_num_covers}, actual: {num_covers}")

            self.assertEqual(expected_num_covers, num_covers)
            self.print_cover_lists(raw_cover_list, cover_list)

            # keys in dictionary returned from raw sql query
            expected_keys = ["author_id", "cover_filepath", "cover_id", "book_id", "artwork_id", "edition_id", "cover_filename"]
            # keys in dictionary returned from django query
            actual_keys = ['author_id', 'cover_filepath', 'cover_id', 'book_id', 'artwork_id', 'edition_id', 'cover_filename']

            #  for each cover: check expected cover data matches actual cover data
            for raw_cover, cover in zip(raw_cover_list, cover_list):
                self.record_matches(raw_cover, expected_keys, cover, actual_keys)

    def test_d_artist_sets_list(self):
        print("===========================================")
        print(f"Test List of Sets for each artist")
        print("===========================================")

        artist_list = self.artist_list_query()
        for artist in artist_list:
            artist_id = artist["artist_id"]

            # return set list as dictionary
            raw_set_list = OriginalRawQuerys.artist_set_list(artist_id, return_dict=True)
            expected_num_sets = len(raw_set_list)

            artist_set_list = CoverQuerys.artist_set_list(artist_id)
            #print(f"artist {artist_id}, set list {artist_set_list}")
            actual_num_sets = len(artist_set_list)

            self.assertEqual(expected_num_sets, actual_num_sets)

            if expected_num_sets > 0:
                print("=============================================")
                print(f"Test {expected_num_sets} sets for artist {artist_id}")
                print(f"artist {artist_id}, set list {artist_set_list}")
                print("==============================================")

                expected_keys = ["set_id", "series_id", "author_id", "artist_id", "imprint_id", "description",
                                 "panorama_id"]

                #  for each set: check expected data matches actual data
                for raw_set, set in zip(raw_set_list, artist_set_list):
                    self.record_matches(raw_set, expected_keys, set, expected_keys)

        print(f"num artists is {len(artist_list)}")

    def test_e_artist_sets_list_covers(self):
        print ("===========================================")
        print (f"Test Covers in each individual Set for each artist")
        print ("===========================================")

        artist_list = self.artist_list_query()
        for artist in artist_list:
            artist_id = artist["artist_id"]
            self.check_artist_set_list(artist_id)

        print (f"num artists is {len(artist_list)}")

    def check_artist_set_list(self, artist_id):
        # return set list as dictionary
        raw_set_list = OriginalRawQuerys.artist_set_list(artist_id, return_dict=True)
        expected_num_sets = len(raw_set_list)

        artist_set_list = CoverQuerys.artist_set_list(artist_id)
        #print(f"artist {artist_id}, set list {artist_set_list}")
        actual_num_sets = len(artist_set_list)

        self.assertEqual(expected_num_sets, actual_num_sets)

        if expected_num_sets > 0:
            print("=============================================")
            print(f"Test {expected_num_sets} sets for artist {artist_id}")
            print(f"author {artist_id}, set list {artist_set_list}")
            print("==============================================")

            #  for each set: check cover data matches actual data
            for set in artist_set_list:
                author_id = set['author_id']
                print (f"author: {author_id}")
                self.check_author_artist_covers_list(author=author_id, artist=artist_id)


class ArtworkQueryTests(QueryTestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json']

    def setUp(self):
        self.subject_model = Artwork
        self.subject_name = "artwork"
        self.pk_name = "artwork_id"
        self.subject_query = CoverQuerys.book_list
        self.original_raw_query = OriginalRawQuerys.artwork_cover_list
        self.all_covers_for_subject = CoverQuerys.all_covers_for_artwork
        # keys in dictionary returned from raw sql query
        self.expected_keys = ["cover_filepath", "cover_filename", "cover_id", "book_id", "edition_id", "artist_id", "artwork_id"]
        # keys in dictionary returned from django query
        self.actual_keys = ["cover_filepath", "cover_filename", "cover_id",
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
        the_book = get_object_or_404(Book, pk=book_id)
        # test covers per artist that did a cover for this book
        artist_list = Artist.objects.filter(theArtwork__book__pk=book_id)
        print (f"the_book is '{the_book}' artist_list is '{artist_list}''")
        for artist in artist_list:
            # we now have a book id and an artist id from which we can get the artwork id
            try:
                artwork = get_object_or_404(Artwork, book_id=book_id, artist_id=artist.pk)
                print("==============================================")
                print(f"artwork is'{artwork}")
                print("==============================================")
                self.artwork_cover_list_matches(the_book, artist, artwork, self.original_raw_query)
            except Artwork.MultipleObjectsReturned:
                # There is at least one instance in which the artist has created different covers for the same book
                # Bruce Pennington, Decision at Doona
                artwork_list = Artwork.objects.filter(book_id=book_id, artist_id=artist.pk)
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

        self.print_cover_lists_simple(raw_cover_list, artwork_cover_list)

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


# python manage.py test bookcovers.tests.test_queries.PrintRunQueryTests --settings=djabbic.testsettings
class PrintRunQueryTests(QueryTestCase):
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
                'SetExceptions.json',
                'PrintRuns.json']

    def test_a_total_num_print_runs(self):
        max_print_run_id = CoverQuerys.highest_print_run()
        print(max_print_run_id['print_run_id__max'])
        highest = max_print_run_id['print_run_id__max'] + 1

        for print_run_id in range(highest):
            original_print_run = OriginalRawQuerys.print_history(print_run_id=print_run_id)
            expected_num_runs = len(original_print_run)

            print_run = CoverQuerys.print_history(print_run_id=print_run_id)
            num_runs = len(print_run)

            try: self.assertEqual(expected_num_runs, num_runs)
            except AssertionError as e:
                # use list to avoid remaining elements truncated
                # otherwise repr is used to represent queryset
                print("================================================================================")
                print(f"Test Total Runs in Print History for {print_run_id}")
                print(f"Expected: {expected_num_runs}, actual: {num_runs}")
                print(f"covers {list(all_list)}")
                print("================================================================================")
                raise

    def test_b_print_runs(self):
        """tests all the runs in all the print_runs"""
        max_print_run_id = CoverQuerys.highest_print_run()
        print(max_print_run_id['print_run_id__max'])
        highest = max_print_run_id['print_run_id__max'] + 1

        for print_run_id in range(highest):
            original_print_run = OriginalRawQuerys.print_history(print_run_id=print_run_id)
            expected_num_runs = len(original_print_run)

            print_run = CoverQuerys.print_history(print_run_id=print_run_id)
            num_runs = len(print_run)

            try: self.assertEqual(expected_num_runs, num_runs)
            except AssertionError as e:
                print ("================================================================================")
                print(f"Test Runs for print run id {print_run_id}")
                print(f"Expected: {expected_num_runs}, actual: {num_runs}")
                print (f"Expected: {expected_record}")
                print (f"Actual: {actual_record}")
                print ("================================================================================")
                raise

            # keys in dictionary returned from raw sql query
            expected_keys = ["print_run_id", "edition_id", "cover_id", "print", "cover_price", "cover_filename", "cover_filepath"]
            # keys in dictionary returned from django query
            actual_keys = ['print_run_id', 'edition_id', 'cover_id', 'print', 'cover_price','cover_filename', 'cover_filepath']

            #  for each cover: check expected cover data matches actual cover data
            for raw_run, run in zip(original_print_run, print_run):
                self.record_matches(raw_run, expected_keys, run, actual_keys)

class PanoramaQueryTests(QueryTestCase):
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
                'SetExceptions.json',
                'PrintRuns.json',
                'Panoramas.json',]

    def setUp(self):
        self.query_cache = QueryCache()

    def test_panoramas(self):
        """tests all panoramas"""

        # return list as dictionary
        raw_panorama_list = OriginalRawQuerys.panorama_list(return_dict=True)
        #print_dict_list(raw_panorama_list)
        expected_num_panoramas = len(raw_panorama_list)

        panorama_list = CoverQuerys.panorama_list()
        print(f"expected number of panoramas is {expected_num_panoramas}, number of panoramas is {len(panorama_list)}")
        #print(f"panorama_list is {panorama_list}")
        num_panoramas = len(panorama_list)

        self.assertEqual(expected_num_panoramas, num_panoramas)

        # keys in dictionary returned from raw sql query
        expected_keys = ['panorama_id', 'order', 'description', 'filename', 'cover_filepath', 'author_name', 'artist_name']
        # keys in dictionary returned from django query
        actual_keys = ['panorama_id', 'order', 'description', 'cover_filename', 'cover_filepath', 'author_name', 'artist_name']


        for expected, panorama in zip(raw_panorama_list, panorama_list):
            self.record_matches(expected, expected_keys, panorama , actual_keys)

    def test_panorama(self):
        """tests individual panorama queries"""
        raw_panorama_list = OriginalRawQuerys.panorama_list(return_dict=True)
        num_panoramas = len(raw_panorama_list)

        print ("==============================================")
        print (f"Test Individual Panoramas. num panoramas {{ num_panoramas }}")
        print ("==============================================")

        # keys in dictionary returned from raw sql query
        expected_keys = ['panorama_id', 'order', 'description', 'filename']
        # keys in dictionary returned from django query
        actual_keys = ['panorama_id', 'order', 'description', 'filename']

        for panorama_entry in range(num_panoramas):
            raw_panorama = OriginalRawQuerys.panorama(panorama_entry, num_panoramas)
            print (f"raw_panorama is {raw_panorama[0]}")
            panorama_id = raw_panorama[0]['panorama_id']
            panorama = self.query_cache.panorama(panorama_id)
            print (f"panorama is {panorama}")

            # test cover filepath from related artist model
            expected_value = raw_panorama[0]['cover_filepath']
            actual_value = panorama.artist.cover_filepath
            #print(f"cover_filepath: expected_value is '{expected_value}', actual_value is '{actual_value}'")
            self.assertEqual(expected_value, actual_value)

            self.entry_matches(raw_panorama[0], expected_keys, panorama, actual_keys)

    def entry_matches(self, expected_record, expected_keys, actual_record, actual_keys):
        # https://docs.python.org/3/library/functions.html#zip
        for expected_key, actual_key in zip(expected_keys, actual_keys):
            expected_value = expected_record[expected_key]
            actual_value = getattr(actual_record, actual_key)
            #print(f"expected_value is '{expected_value}', actual_value is '{actual_value}'")
            try: self.assertEqual(expected_value, actual_value)
            except AssertionError as e:
                print ("================================================================================")
                print (f"Expected: {expected_record}")
                print (f"Actual: {actual_record}")
                print ("================================================================================")
                raise

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
                'SetExceptions.json',
                'PrintRuns.json',
                'Panoramas.json',
                'AuthorAkas',]

    def test_author_aka_list_of_covers(self):
        # Robert Heinlein
        author_id = 4

        raw_cover_list = OriginalRawQuerys.author_cover_list(author_id, True)
        print_dict_list(raw_cover_list)
        print(f"num entries is {len(raw_cover_list)}")

        author = Author.objects.get(pk=author_id)
        django_cover_list = CoverQuerys.all_covers_of_all_books_for_author(author=author, author_id=author_id)
        print_dict_list(django_cover_list)
        print(f"num entries is {len(django_cover_list)}")

    # def test_num_covers_in_artist_sets(self):
    #     # Brian Cronin
    #     artist_id = 139
    #
    #     original_cover_list = OriginalRawQuerys.artist_set_cover_list(artist_id, return_dict=True)
    #     expected_num_covers = len(original_cover_list)
    #
    #     all_list = CoverQuerys.artist_set_covers(artist_id=artist_id)
    #     num_covers = len(all_list)
    #
    #     if expected_num_covers != 0 or num_covers != 0:
    #         print("==============================================")
    #         print(f"Test Total Covers in sets for artist {artist_id}")
    #         print("==============================================")
    #         print(f"Expected: {expected_num_covers}, actual: {num_covers}")
    #
    #     try: self.assertEqual(expected_num_covers, num_covers)
    #     except AssertionError as e:
    #         # use list to avoid remaining elements truncated
    #         # otherwise repr is used to represent queryset
    #         print("================================================================================")
    #         print(f"covers {list(all_list)}")
    #         print("================================================================================")
    #         raise


    # def test_artwork_set(self):
    #     # Ray Bradbury, Josh Kirby settings
    #     author_id = 15
    #     artist_id = 35
    #     expected_num_covers = 2
    #     set_id = 4
    #
    #     # Frank Herbert , Gerry Grace settings
    #     author_id = 5
    #     artist_id = 28
    #     expected_num_covers = 5
    #     set_id = 14
    #
    #     # Elizabeth Moon
    #     # author_id = 104
    #     # expected_num_covers = 9
    #     # set_id = 16
    #
    #     # Ray Bradbury, Bruce Pennington settings
    #     author_id = 15
    #     artist_id = 2
    #     expected_num_covers = 7
    #     set_id = 3
    #
    #     print("==============================================")
    #     print(f"Test Set Covers for set {set_id}")
    #     print("==============================================")
    #     set, set_cover_list = CoverQuerys.author_artist_set_cover_list(set_id=set_id)
    #     num_covers = len(set_cover_list)
    #
    #     print(f"Expected: {expected_num_covers}, actual: {num_covers}")
    #     print_dict_list(list(set_cover_list))
    #     try: self.assertEqual(expected_num_covers, num_covers)
    #     except AssertionError as e:
    #         # use list to avoid remaining elements truncated
    #         # otherwise repr is used to represent queryset
    #         print("================================================================================")
    #         print(f"Expected: {expected_num_covers}, actual: {num_covers}")
    #         print("set_cover_list is")
    #         print_dict_list(list(set_cover_list))
    #         print("================================================================================")
    #         raise


    # def test_set_covers(self):
    #
    #     # Ray Bradbury, Bruce Pennington settings
    #     author_id = 15
    #     artist_id = 2
    #     expected_num_covers = 7
    #
    #     # Ray Bradbury, Josh Kirby settings
    #     author_id = 15
    #     artist_id = 35
    #     expected_num_covers = 2
    #
    #     # Frank Herbert , Gerry Grace settings
    #     author_id = 5
    #     artist_id = 28
    #     expected_num_covers = 5
    #
    #     # Elizabeth Moon
    #     # author_id = 104
    #     # expected_num_covers = 9
    #
    #     print("==============================================")
    #     print(f"Test Set Covers for author {author_id}, artist {artist_id}")
    #     print("==============================================")
    #     original_cover_list = OriginalRawQuerys.author_artist_set_cover_list(author_id, artist_id, return_dict=True)
    #     print("original_cover_list is")
    #     print_dict_list(original_cover_list)
    #     original_num_covers = len(original_cover_list)
    #     print(f"original number of covers is {original_num_covers}")
    #     set_cover_list = CoverQuerys.author_artist_set_cover_list(author_id=author_id, artist_id=artist_id)
    #     num_covers = len(set_cover_list)
    #
    #     print(f"Expected: {expected_num_covers}, original: {original_num_covers}, actual: {num_covers}")
    #     print_dict_list(list(set_cover_list))
    #     try: self.assertEqual(expected_num_covers, original_num_covers)
    #     except AssertionError as e:
    #         # use list to avoid remaining elements truncated
    #         # otherwise repr is used to represent queryset
    #         print("================================================================================")
    #         print(f"Expected: {expected_num_covers}, actual: {num_covers}")
    #         print("set_cover_list is")
    #         print_dict_list(list(set_cover_list))
    #         print("================================================================================")
    #         raise

    # def test_author_books(self):
    #     author_id = 5
    #     print ("==============================================")
    #     print (f"Test List of Books for author {author_id}")
    #     print ("==============================================")
    #     author = get_object_or_404(Author, pk=author_id)
    #     book_list = CoverQuerys.books_for_author(author)
    #     print(f"number of books is {len(book_list)}")
    #     print(f"book_list is {book_list}")
    #
    #     for book in book_list:
    #         print (f"book is '{book}'")

    # def test_print_run(self):
    #     print_run_id = 7
    #
    #     print ("==============================================")
    #     print (f"Test Print Run for {print_run_id}")
    #     print ("==============================================")
    #     original_print_run = OriginalRawQuerys.print_history(print_run_id=print_run_id)
    #     print_dict_list(original_print_run)
    #     print (f"num entries is {len(original_print_run)}")
    #
    #     print_run = CoverQuerys.print_history(print_run_id=print_run_id)
    #     print(f"print_run is {print_run}")


