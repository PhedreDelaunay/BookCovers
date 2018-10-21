from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.conf import settings


from bookcovers.models import Artists
from bookcovers.models import Authors
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

class AuthorQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'AuthorAkas.json']

    def test_author_name(self):
        author = Authors.objects.get(pk=6)
        expected_author_name = "Philip K. Dick"
        self.assertEqual(expected_author_name, author.name)

    # test author list
    def test_author_alist(self):
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

    def cover_matches(self, expected_cover, actual_cover):
        # keys in dictionary returned from raw sql query
        expected_keys = ["book_id", "cover_filepath", "cover_filename", "copyright_year"]
        # keys in dictionary returned from django query
        actual_keys = ["book_id", "cover__artwork__artist__cover_filepath", "cover__cover_filename", "copyright_year"]
        # print (f"Expected: {expected_cover}")
        # print (f"Actual: {actual_cover}")

        self.record_matches(expected_cover, expected_keys, actual_cover, actual_keys)
        
    # test author cover list
    def author_cover_list_matches(self, author):
        # return cover list as dictionary
        raw_cover_list = OriginalRawQuerys.author_cover_list(author.pk, True)
        expected_num_covers = len(raw_cover_list)

        #print(f"cover_filepath is {artist.cover_filepath}")
        cover_list = CoverQuerys.author_cover_list(author, test=True)
        num_covers = len(cover_list)
        print (f"author cover_list is:\n {cover_list}")

        print (f"expected_num_covers is {expected_num_covers}, num_covers is {num_covers}")

        self.print_cover_lists(raw_cover_list, cover_list)
        try: self.assertEqual(expected_num_covers, num_covers)
        except AssertionError as e:
            print (f"author cover_list query is:\n{cover_list.query}")
            raise

        #  for each cover: check expected cover data matches actual cover data
        for raw_cover, cover in zip(raw_cover_list, cover_list):
            self.cover_matches(raw_cover, cover)

    def author_cover(self, author_id=None):
        the_author = get_object_or_404(Authors, pk=author_id)
        self.author_cover_list_matches(the_author)

    # def test_author_cover(self):
    #     self.author_cover(6)

    def test_author_cover_list(self):
        author_list = CoverQuerys.author_list()

        for author in author_list:
            author_id = author['author_id']
            print (f"author_id is {author_id}")
            self.author_cover(author_id)



class ArtistQueryTests(SubjectQueryTest):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'ArtistAkas.json']

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
        actual_keys = ["book", "cover__cover_filename", "year"]
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


