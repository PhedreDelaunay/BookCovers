from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.conf import settings


from bookcovers.models import Artists
from bookcovers.models import Authors
from bookcovers.original_raw_querys import OriginalRawQuerys
from bookcovers.cover_querys import CoverQuerys

# Using the unittest framework to test the django queries against the original raw sql queries

class AuthorQueryTests(TestCase):
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


class ArtistQueryTests(TestCase):
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

    def item_matches(self, expected_record, expected_key, actual_record, actual_key):
        expected_value = expected_record[expected_key]
        actual_value= actual_record.get(actual_key, actual_key)
        print ("expected_value is '{}', actual_value is '{}'".format(expected_value, actual_value))
        self.assertEqual(expected_value, actual_value)

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

    # test artist list
    def artist_matches(self, expected_artist, actual_artist):
        # keys in dictionary returned from raw sql query
        expected_keys = ["artist_id", "name"]
        # keys in dictionary returned from django query
        actual_keys = ["artist_id", "name"]
        self.record_matches(expected_artist, expected_keys, actual_artist, actual_keys)

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

        for raw_artist_list, artist_list in zip(raw_artist_list, artist_list):
            self.artist_matches(raw_artist_list, artist_list)

    # test artist cover list
    def cover_matches(self, expected_cover, actual_cover):
        # keys in dictionary returned from raw sql query
        expected_keys = ["book_id", "cover_filename", "year"]
        # keys in dictionary returned from django query
        actual_keys = ["book", "cover__cover_filename", "year"]
        # print (f"Expected: {expected_cover}")
        # print (f"Actual: {actual_cover}")

        self.record_matches(expected_cover, expected_keys, actual_cover, actual_keys)

    def print_cover_lists(self, raw_cover_list, cover_list):
        for raw_cover in raw_cover_list:
            print(f"raw book_id is {raw_cover['book_id']}")
        for cover in cover_list:
            cover_dict = "".join(str(key) + ':' + str(value) + ', ' for key, value in cover.items())
            print(cover_dict)

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


