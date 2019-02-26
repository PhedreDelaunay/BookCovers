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
                    'Series.json']

        def check_status_code(self, reverse_url):
            print ("----------------------------------")
            print (f"check_status_code: {self.test_class_name}")
            print ("----------------------------------")
            response = self.client.get(reverse_url)
            self.assertEquals(response.status_code, 200, msg=f"reverse_url: {reverse_url}")

        def check_template(self, reverse_url, template_url):
            print ("----------------------------------")
            print (f"check_template: {self.test_class_name}")
            print ("----------------------------------")
            response = self.client.get(reverse_url)
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, template_url)

        def test_status_code(self):
            self.check_status_code(reverse_url=self.reverse_url)

        def test_template(self):
            self.check_template(reverse_url=self.reverse_url, template_url=self.template_url)


class ArtistListPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.test_class_name = "ArtistListPageTest"
        self.reverse_url = reverse('bookcovers:artists')
        self.template_url = 'bookcovers/artist_list.html'


class ArtistPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.test_class_name = "ArtistPageTest"
        self.reverse_url = reverse('bookcovers:artist_books', kwargs={'artist_id': 6})
        self.template_url = 'bookcovers/artist_book_covers.html'

    def test_status_code_name(self):
        reverse_url = reverse('bookcovers:artist_books', kwargs={'name': 'Jim Burns'})
        self.check_status_code(reverse_url=reverse_url)

    def test_status_code_slug(self):
        reverse_url = reverse('bookcovers:artist_books', kwargs={'slug': 'Jim-Burns'})
        self.check_status_code(reverse_url=reverse_url)

class ArtworkPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.test_class_name = "ArtworkPageTest"
        self.reverse_url = reverse('bookcovers:artwork', kwargs={'artwork_id': 178})
        self.template_url = 'bookcovers/artist_books_per_artwork.html'

class AuthorListPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.test_class_name = "AuthorListPageTest"
        self.reverse_url = reverse('bookcovers:authors')
        self.template_url = 'bookcovers/author_list.html'


class AuthorPageTest(PageTestCases.PageTestCase):

    def setUp(self):
        self.test_class_name = "AuthorPageTest"
        self.reverse_url = reverse('bookcovers:author_books', kwargs={'author_id': 4})
        self.template_url = 'bookcovers/author_book_covers.html'

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
        self.test_class_name = "AuthorSetsPageTest"
        self.reverse_url = reverse('bookcovers:author_book_sets', kwargs={'name': 'Ray Bradbury'})
        #self.reverse_url = reverse('bookcovers:author_book_sets', kwargs={'author_id': 15})
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
        self.test_class_name = "BookPageTest"
        self.reverse_url = reverse('bookcovers:book_covers', kwargs={'book_id': 93})
        self.template_url = 'bookcovers/author_covers_per_book.html'
