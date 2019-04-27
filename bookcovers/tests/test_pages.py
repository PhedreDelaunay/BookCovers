from django.test import TestCase
from django.urls import reverse

from bookcovers.models import Artist
from bookcovers.models import Author
from bookcovers.models import Book
from bookcovers.models import Cover
from bookcovers.models import Artwork

from bookcovers.cover_querys import CoverQuerys

# https://docs.djangoproject.com/en/2.1/topics/testing/tools/
# https://docs.djangoproject.com/en/2.1/topics/http/urls/
# It is strongly desirable to avoid hard-coding these URLs (a laborious, non-scalable and error-prone strategy
# Use reverse resolution of urls which makes use of the view name and any arguments

# https://stackoverflow.com/questions/1323455/python-unit-test-with-base-and-sub-class
# unittest only runs module-level classes that inherit from TestCase.
# Wrap PageTestCase in a blank class so that it is not module level and the unittest framework will not attempt
# to run the test methods without any data
class PageTestCases:

    class PageTestCase(TestCase):
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
                    'BooksSeries.json',]

        def check_status_code(self, reverse_url):
            print ("----------------------------------")
            print (f"check_status_code: {type(self).__name__}")
            print ("----------------------------------")
            response = self.client.get(reverse_url)
            self.assertEquals(response.status_code, self.expected_response_code, msg=f"reverse_url: {reverse_url}")

        def check_template(self, reverse_url, template_url):
            print ("----------------------------------")
            print (f"check_template: {type(self).__name__}")
            print ("----------------------------------")
            response = self.client.get(reverse_url)
            print (f"response.status_code is {response.status_code}")
            self.assertEquals(response.status_code, self.expected_response_code)
            self.assertTemplateUsed(response, template_url)

        def test_status_code(self):
            self.check_status_code(reverse_url=self.reverse_url)

        def test_template(self):
            self.check_template(reverse_url=self.reverse_url, template_url=self.template_url)


class ArtistListPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artists/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artists')
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artist_list.html'


class ArtistPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artist/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artist_artworks', kwargs={'artist_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artist_artworks.html'

    # TODO
    # test sets link appears in artist, Bruce Pennington, known to have sets
    # https://docs.djangoproject.com/en/2.1/topics/testing/tools/
    def test_page_contains_sets_link(self):
        # ex: /bookcovers/artist/Bruce%20Pennington/
        sets_reverse_url = reverse('bookcovers:artist_sets', kwargs={'name':'Bruce Pennington'})
        #print (f'reverse_url is "{reverse_url}"')
        response = self.client.get(reverse('bookcovers:artist_artworks', kwargs={'name':'Bruce Pennington'}))
        self.assertContains(response, f'href="{sets_reverse_url}">', count=1, status_code=200, msg_prefix='', html=False)

    # test sets link does not appear in artist
    # https://docs.djangoproject.com/en/2.1/topics/testing/tools/
    def test_page_notcontains_sets_link(self):
        # ex: /bookcovers/artist/David%20Hardy/
        sets_reverse_url = reverse('bookcovers:artist_sets', kwargs={'name':'David Hardy'})
        response = self.client.get(reverse('bookcovers:artist_artworks', kwargs={'name':'David Hardy'}))
        self.assertNotContains(response, f'href="{sets_reverse_url}">', status_code=200, msg_prefix='', html=False)

    def test_status_code_name(self):
        # ex: /bookcovers/artist/Jim%20Burns/
        reverse_url = reverse('bookcovers:artist_artworks', kwargs={'name': 'Jim Burns'})
        self.check_status_code(reverse_url=reverse_url)

    def test_status_code_slug(self):
        # ex: /bookcovers/artist/Jim-Burns/
        reverse_url = reverse('bookcovers:artist_artworks', kwargs={'slug': 'Jim-Burns'})
        self.check_status_code(reverse_url=reverse_url)


class ArtistSetsPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artist/Bruce%20Pennington/sets/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artist_sets', kwargs={'name': 'Bruce Pennington'})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artist_sets.html'


class ArtworkPageTest(PageTestCases.PageTestCase):
    # /bookcovers/artwork/178/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork', kwargs={'artwork_id': 178})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artwork_cover.html'

        # TODO test for thumnbails, no thumbnails


class ArtworkEditionPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artwork/edition/7/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork_edition', kwargs={'edition_id': 7})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artwork_cover.html'

        # TODO test for thumnbails, no thumbnails

class ArtworkListPageTest(PageTestCases.PageTestCase):
    # /bookcovers/artworks/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artworks', kwargs={'artwork_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artworks.html'


class ArtworkSetEditionPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artwork/set/edition/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork_set_edition', kwargs={'edition_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_edition.html'

    # TODO test for thumnbails, no thumbnails

class ArtworkSetDetailPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artwork/set/detail/3/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork_set_detail', kwargs={'set_id': 3})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_edition.html'

    # TODO test for thumnbails, no thumbnails

class ArtworkSetEditionsPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artwork/set/editions/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork_set_editions', kwargs={'edition_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_editions.html'

class ArtworkSetListPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/artwork/set/list/3/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork_set_list', kwargs={'set_id': 3})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_editions.html'


#========================================================
class AuthorListPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/authors/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:authors')
        self.expected_response_code = 200
        self.template_url = 'bookcovers/author_list.html'


class AuthorPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/author/4/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:author_books', kwargs={'author_id': 4})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/author_books.html'

    # test sets link appears in author, Ray Bradbury, known to have sets
    # https://docs.djangoproject.com/en/2.1/topics/testing/tools/
    def test_page_contains_sets_link(self):
        # ex: /bookcovers/author/Ray%20Bradbury/
        sets_reverse_url = reverse('bookcovers:author_sets', kwargs={'name':'Ray Bradbury'})
        #print (f'reverse_url is "{reverse_url}"')
        response = self.client.get(reverse('bookcovers:author_books', kwargs={'name':'Ray Bradbury'}))
        self.assertContains(response, f'href="{sets_reverse_url}">', count=1, status_code=200, msg_prefix='', html=False)

    # test sets link does not appear in author, Rex Gordon, known  not to have sets
    # https://docs.djangoproject.com/en/2.1/topics/testing/tools/
    def test_page_notcontains_sets_link(self):
        # ex: /bookcovers/author/Rex%20Gordon/
        sets_reverse_url = reverse('bookcovers:author_sets', kwargs={'name':'Rex Gordon'})
        response = self.client.get(reverse('bookcovers:author_books', kwargs={'name':'Rex Gordon'}))
        self.assertNotContains(response, f'href="{sets_reverse_url}">', status_code=200, msg_prefix='', html=False)

    def test_status_code_name(self):
        # ex: /bookcovers/author/Robert%20Heinlein/
        reverse_url = reverse('bookcovers:author_books', kwargs={'name': 'Robert Heinlein'})
        self.check_status_code(reverse_url=reverse_url)

    def test_status_code_slug(self):
        # ex: /bookcovers/author/Robert-Heinlein/
        reverse_url = reverse('bookcovers:author_books', kwargs={'slug': 'Robert-Heinlein'})
        self.check_status_code(reverse_url=reverse_url)


class AuthorSetsPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/author/Ray%20Bradbury/sets/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:author_sets', kwargs={'name': 'Ray Bradbury'})
        #self.reverse_url = reverse('bookcovers:author_book_sets', kwargs={'author_id': 15})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/author_sets.html'

    # def test_status_code_name(self):
    #     reverse_url = reverse('bookcovers:author_book_sets', kwargs={'name': 'Ray Bradbury'})
    #     self.check_status_code(reverse_url=reverse_url)
    #
    # def test_status_code_slug(self):
    #     reverse_url = reverse('bookcovers:author_book_sets', kwargs={'slug': 'Ray-Bradbury'})
    #     self.check_status_code(reverse_url=reverse_url)


class BookPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/book/174/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:book', kwargs={'book_id': 174})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/book.html'

        # TODO test for thumnbails, no thumbnails
        # /bookcovers/book/8/

class BookEditionPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/book/edition/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:book_edition', kwargs={'edition_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/book.html'

    # TODO test for thumnbails, no thumbnails


class BookSetEditionPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/book/set/edition/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:set_edition', kwargs={'edition_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_edition.html'

    # TODO test for thumnbails, no thumbnails

class BookSetDetailPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/book/set/detail/3/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:book_set_detail', kwargs={'set_id': 3})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_edition.html'

    # TODO test for thumnbails, no thumbnails

class BookSetEditionsPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/book/set/editions/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:set_editions', kwargs={'edition_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_editions.html'

class BookSetListPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/book/set/editions/6/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:book_set_list', kwargs={'set_id': 3})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/set_editions.html'


class BooksPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/books/93/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:books', kwargs={'book_id': 93})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/books.html'


class PrintHistoryPageTest(PageTestCases.PageTestCase):
    # ex: /bookcovers/print_run/7/
    def setUp(self):
        self.reverse_url = reverse('bookcovers:print_history', kwargs={'print_run_id': 7})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/print_history.html'