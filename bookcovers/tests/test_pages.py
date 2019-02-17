from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import F

from bookcovers.models import Artists
from bookcovers.models import Authors
from bookcovers.models import Books
from bookcovers.models import Covers
from bookcovers.models import Artworks

from bookcovers.cover_querys import CoverQuerys

class ArtistListPageTest(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',]

    def test_status_code(self):
        response = self.client.get('/bookcovers/artists/')
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/bookcovers/artists/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookcovers/artist_list.html')

class ArtistPageTest(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',]

    def test_status_code(self):
        response = self.client.get('/bookcovers/artist/6/')
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/bookcovers/artist/Jim%20Burns/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookcovers/artist_book_covers.html')

class ArtworkPageTest(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',]

    def test_status_code(self):
        response = self.client.get('/bookcovers/artwork/178/')
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/bookcovers/artwork/178/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookcovers/artist_books_per_artwork.html')

class AuthorListPageTest(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',]

    def test_status_code(self):
        response = self.client.get('/bookcovers/authors/')
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/bookcovers/authors/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookcovers/author_list.html')

class AuthorPageTest(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',]

    def test_status_code(self):
        response = self.client.get('/bookcovers/author/4/')
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/bookcovers/author/Robert%20Heinlein/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookcovers/author_book_covers.html')

class AuthorSetsPageTest(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',
                'Sets.json',
                'Series.json',]

    def test_status_code(self):
        response = self.client.get('/bookcovers/author/Ray%20Bradbury/sets')
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/bookcovers/author/Ray%20Bradbury/sets')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookcovers/author_book_sets.html')

    # test Ray Bradbury for sets and another author for no sets

class BookPageTest(TestCase):
    fixtures = ['Artists.json',
                'Artworks.json',
                'Authors.json',
                'Books.json',
                'Editions.json',
                'Covers.json',
                'Countries.json',]

    def test_status_code(self):
        response = self.client.get('/bookcovers/book/93/')
        self.assertEquals(response.status_code, 200)

    def test_template(self):
        response = self.client.get('/bookcovers/book/93/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookcovers/author_covers_per_book.html')