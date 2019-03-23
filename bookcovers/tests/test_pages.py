from django.test import TestCase
from django.urls import reverse

from bookcovers.models import Artists
from bookcovers.models import Author
from bookcovers.models import Books
from bookcovers.models import Covers
from bookcovers.models import Artworks

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

    def setUp(self):
        self.reverse_url = reverse('bookcovers:artists')
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artist_list.html'


class ArtistPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:artist_artworks', kwargs={'artist_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artist_artworks.html'

    def test_status_code_name(self):
        reverse_url = reverse('bookcovers:artist_artworks', kwargs={'name': 'Jim Burns'})
        self.check_status_code(reverse_url=reverse_url)

    def test_status_code_slug(self):
        reverse_url = reverse('bookcovers:artist_artworks', kwargs={'slug': 'Jim-Burns'})
        self.check_status_code(reverse_url=reverse_url)

class ArtworkPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork', kwargs={'artwork_id': 178})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artwork.html'

class ArtworkListPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:artwork', kwargs={'artwork_id': 6})
        self.expected_response_code = 302

    def test_template(self):
        self.reverse_url = reverse('bookcovers:artwork_list', kwargs={'artwork_id': 6})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/artwork_list.html'
        super().test_template()

class AuthorListPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:authors')
        self.expected_response_code = 200
        self.template_url = 'bookcovers/author_list.html'


class AuthorPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:author_books', kwargs={'author_id': 4})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/author_books.html'

    # test sets link appears in author, Ray Bradbury, known to have sets
    # https://docs.djangoproject.com/en/2.1/topics/testing/tools/
    def test_page_contains_sets_link(self):
        sets_reverse_url = reverse('bookcovers:author_book_sets', kwargs={'name':'Ray Bradbury'})
        #print (f'reverse_url is "{reverse_url}"')
        response = self.client.get(reverse('bookcovers:author_books', kwargs={'name':'Ray Bradbury'}))
        self.assertContains(response, f'href="{sets_reverse_url}">', count=1, status_code=200, msg_prefix='', html=False)

    # test sets link does not appear in author, Rex Gordon, known  not to have sets
    # https://docs.djangoproject.com/en/2.1/topics/testing/tools/
    def test_page_notcontains_sets_link(self):
        sets_reverse_url = reverse('bookcovers:author_book_sets', kwargs={'name':'Rex Gordon'})
        response = self.client.get(reverse('bookcovers:author_books', kwargs={'name':'Rex Gordon'}))
        self.assertNotContains(response, f'href="{sets_reverse_url}">', status_code=200, msg_prefix='', html=False)

    def test_status_code_name(self):
        reverse_url = reverse('bookcovers:author_books', kwargs={'name': 'Robert Heinlein'})
        self.check_status_code(reverse_url=reverse_url)

    def test_status_code_slug(self):
        reverse_url = reverse('bookcovers:author_books', kwargs={'slug': 'Robert-Heinlein'})
        self.check_status_code(reverse_url=reverse_url)


class AuthorSetsPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:author_book_sets', kwargs={'name': 'Ray Bradbury'})
        #self.reverse_url = reverse('bookcovers:author_book_sets', kwargs={'author_id': 15})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/author_book_sets.html'

    # def test_status_code_name(self):
    #     reverse_url = reverse('bookcovers:author_book_sets', kwargs={'name': 'Ray Bradbury'})
    #     self.check_status_code(reverse_url=reverse_url)
    #
    # def test_status_code_slug(self):
    #     reverse_url = reverse('bookcovers:author_book_sets', kwargs={'slug': 'Ray-Bradbury'})
    #     self.check_status_code(reverse_url=reverse_url)


class BookPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:book', kwargs={'book_id': 174})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/book.html'

class BookListPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.reverse_url = reverse('bookcovers:book', kwargs={'book_id': 93})
        self.expected_response_code = 302

    def test_template(self):
        self.reverse_url = reverse('bookcovers:book_list', kwargs={'book_id': 93})
        self.expected_response_code = 200
        self.template_url = 'bookcovers/book_list.html'
        super().test_template()