import os

from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.conf import settings

from bookcovers.models import Artists
from bookcovers.cover_querys import CoverQuerys

# Using the unittest framework to identify missing images

class ImageTests(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'ArtistAkas.json']

    # test that cover images are there
    def image_exists(self,absolute_image_filepath):
        try: self.assertTrue(os.path.exists(absolute_image_filepath))
        except AssertionError as e:
            print("absolute_image_filepath is {}".format(absolute_image_filepath))
            #raise

    def get_absolute_path(self,image):
        if settings.STATIC_ROOT:
            absolute_image_filepath = os.path.join(settings.STATIC_ROOT, image)
        elif settings.STATICFILES_DIRS:
            # loop through each line in list
            for dir in settings.STATICFILES_DIRS:
                absolute_image_filepath = os.path.join(dir, image)
                if os.path.exists(absolute_image_filepath):
                    break

        return absolute_image_filepath


    def cover_images_exist(self, artist):
        cover_list = CoverQuerys.artist_cover_list(artist)
        for cover in cover_list:
            thumbnail = "".join([artist.cover_filepath,"Thumbnails/",cover['cover__cover_filename']])
            # print ("thumbnail is {}".format(thumbnail))
            absolute_image_filepath = self.get_absolute_path(thumbnail)
            self.image_exists(absolute_image_filepath)

            cover_image = "".join([artist.cover_filepath,cover['cover__cover_filename']])
            # print ("cover_image is {}".format(cover_image))
            absolute_image_filepath = self.get_absolute_path(cover_image)
            self.image_exists(absolute_image_filepath)


    def test_cover_images(self):
        artist_list = CoverQuerys.artist_list()

        for artist in artist_list:
            artist_id = artist['artist_id']
            # print ("artist_id is {}".format(artist_id))
            the_artist = get_object_or_404(Artists, pk=artist_id)
            self.cover_images_exist(the_artist)