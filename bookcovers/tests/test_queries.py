from django.test import TestCase

from bookcovers.models import Artists

class ArtistQueryTests(TestCase):
    fixtures = ['Artists.json']

    def test_artist_name(self):
        artist = Artists.objects.get(pk=83)
        expected_artist_name = f'Tony Roberts'
        self.assertEquals(expected_artist_name, f'{artist.name}')
