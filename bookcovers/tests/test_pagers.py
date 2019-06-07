from django.test import TestCase

from bookcovers.pagers import ArtistPager
from bookcovers.cover_querys import CoverQuerys
from bookcovers.models import Artist

class PagerTestCases:

    class PagerTestCase(TestCase):
        fixtures = ['Artists.json',
                    'Artworks.json',
                    'Authors.json',
                    'Books.json',
                    'Editions.json',
                    'Covers.json',
                    'Countries.json',
                    'Sets.json',
                    'Series.json',
                    'SetExceptions.json',
                    'BooksSeries.json',
                    'PrintRuns.json',]

        def test_return_to_all(self):
            pass

        def test_first_page(self):
            pass

        def test_previous_page(self):
            pass

        def test_page_number(self):
            pass

        def test_total_num_pages(self):
            pass

        def test_next_page(self):
            pass

        def test_last_page(self):
            pass

        def test_pager_is_displayed(self):
            pass


class ArtistPagerTest(PagerTestCases.PagerTestCase):
    def setUp(self):

        #artist_pager = ArtistPager(self.query_cache, page_number=page_number, artist_id=artist_id, name=name, slug=slug)
        pass