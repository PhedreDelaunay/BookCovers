from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from bookcovers.models import Artists
from bookcovers.models import Artworks

def transform_slug(slug):
    slug = slug.replace('__', '%')
    slug = slug.replace('-', ' ')
    slug = slug.replace('%', '-')

    return slug

class SubjectPager():
    """
    Pager for top level subject, ie artist, author,
    """
    def __init__(self, page=None, subject_id=None, name=None, slug=None):
        """
        :param page:            current page if set
        one of
        :param subject_id:      artist or author id
        :param name:            artist or author name
        :param slug:            artist or author slug
        """
        self.page = page
        self.subject_id = subject_id
        self.name = name
        self.slug = slug

    def pager(self, cover_query, subject_id_key, subject_model):
        """
        :param cover_query:         query to get list of items to page
        :param subject_id_key:      key of id; artist_id, author_id
        :param subject_model:       model for item; Artists, Authors
        :return:
        """
        # TODO can queries be cached between pages?
        subject_list = cover_query()

        # Show 1 cover work per page
        paginator = Paginator(subject_list, 1)

        # have we got here by paging?
        if self.page:
            print(f"subject_list[{self.page}-1] is {subject_list[int(self.page)-1]}")
            kwargs = {'pk': subject_list[int(self.page) - 1][subject_id_key]}
        else:
            if self.subject_id:
                kwargs = {'pk': self.subject_id}
            elif self.name:
                kwargs = {'name': self.name}
            elif self.slug:
                slug = transform_slug(self.slug)
                kwargs = {'name': slug}

        for key, value in kwargs.items():
            print (f"key {key} is '{value}'")

        self.entry = get_object_or_404(subject_model, **kwargs)
        if not self.page:
            # Which page is the requested entry?
            page = [count for count, record in enumerate(subject_list, 1) if record[subject_id_key] == self.entry.pk]
            self.page = int(page[0])
            print (f"SubjectPager figured out that page is {self.page}")

        subject_pager = paginator.get_page(self.page)
        return subject_pager

    def get_entry(self):
        return self.entry


class BookPager():
    """
    Pager for second level book list,
    ie book covers for artwork (from artist) or book covers for book title (from author)
    """
    def __init__(self, page=None, subject_id=None):
        """
        :param page:            current page if set
        one of
        :param subject_id:      artwork or book id
        """
        self.page = page
        self.subject_id = subject_id

    def pager(self, book_cover_query, query_kwargs, subject_id_key, subject_model):
        """
        :param book_cover_query:    query to get list of book covers to page
        :param subject_id_key:      string key of id; artwork_id, book_id
        :param subject_model:       model for item; Artworks, Books
        :return:
        """
        # have we got here by paging?
        if not self.page:
            if self.subject_id:
                kwargs = {'pk': self.subject_id}
                #self.entry = get_object_or_404(subject_model, **kwargs)
                print (f"self.subject_id is '{self.subject_id}'")


        # book_cover_list = CoverQuerys.artist_cover_list(artist=artist)
        # artwork = get_object_or_404(Artworks, artwork_id=artwork_id)
        # book_cover_list = CoverQuerys.all_covers_of_all_books_for_author(author=author, all=False)
        # book = get_object_or_404(Books, pk=book_id)
        #book_cover_list = book_cover_query(**query_kwargs)
        artwork = get_object_or_404(Artworks, artwork_id=self.subject_id)
        artist = get_object_or_404(Artists, artist_id=artwork.artist.pk)
        book_cover_list = book_cover_query(artist=artist)

        print (f"BookPager page is {self.page}")
        if self.page:
            print(f"book_cover_list[{self.page}-1] is {book_cover_list[int(self.page)-1]}")
            kwargs = {'pk': book_cover_list[int(self.page) - 1][subject_id_key]}
            self.entry = get_object_or_404(subject_model, **kwargs)
        else:
            self.entry = artwork

        # Show 1 book title per page
        paginator = Paginator(book_cover_list, 1)

        if not self.page:
            # Which page is the requested entry?
            page = [count for count, record in enumerate(book_cover_list, 1) if record[subject_id_key] == artwork.pk]
            self.page = int(page[0])
            print (f"BookPager figured out that page is {self.page}")

        book_pager = paginator.get_page(self.page)
        return book_pager

    def get_entry(self):
        return self.entry