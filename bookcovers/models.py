# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.functional import cached_property

import collections

# https://docs.djangoproject.com/en/2.0/intro/tutorial02/
# It’s important to add __str__() methods to your models, 
# not only for your own convenience when dealing with the interactive prompt, 
# but also because objects’ representations are used throughout Django’s automatically-generated admin.


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    cover_filepath = models.CharField(max_length=128, blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    birthplace = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artists'
        # sort alphabetically in admin
        ordering = ('name',)

class ArtistAka(models.Model):
    artist_aka_id = models.IntegerField()
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtist_akas", related_query_name="theArtist_aka")
    #artist = models.IntegerField(db_column='artist_id')

    def __str__(self):
        return self.artists.name

    class Meta:
        db_table = 'artist_akas'

#class AuthorManager(models.Manager):
#    def get_by_natural_key(self, fullname):
#        return self.get(fullname=fullname)

class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=100, blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=128, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    birthplace = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        # getframe_expr = 'sys._getframe({}).f_code.co_name'
        # caller = eval(getframe_expr.format(11))
        # callers_caller = eval(getframe_expr.format(12))
        # print(f"I was called from '{caller}'")
        # print(f"{caller}, was called from '{callers_caller}'")
        # technical_500_response, was called from 'handle_uncaught_exception
        # render, was called from 'author_book_sets'
        print(self.__dict__)

    class Meta:
        db_table = 'authors'
        # sort alphabetically in admin
        ordering = ('name',)


class AuthorAka(models.Model):
    # pk=id is implied
    author_aka_id = models.IntegerField()
    author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True,
                               related_name="theAuthor_akas", related_query_name="theAuthor_aka")
    real_name = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.author.name

    class Meta:
        db_table = 'author_akas'


# https://docs.djangoproject.com/en/2.0/topics/db/queries/#backwards-related-objects
# if a model has a ForeignKey, instances of the foreign-key model will have access to a Manager 
# that returns all instances of the first model. 
# By default, this Manager is named FOO_set, where FOO is the source model name, lowercased
# You can override the FOO_set name by setting the related_name parameter in the ForeignKey definition
# related_query_name creates a relation from the related object back to this one. This allows querying and filtering from the related object.
class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True,
                               related_name="theBooks", related_query_name="theBook")
    title = models.CharField(unique=True, max_length=50, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    copyright_year = models.IntegerField(blank=True, null=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    quick_notes = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title

    @cached_property
    def get_creator(self):
        return self.author

    class Meta:
        db_table = 'books'
        # sort alphabetically in admin
        ordering = ('title',)


# https://docs.djangoproject.com/en/2.0/topics/db/queries/#backwards-related-objects
# override the FOO_set name (artworks_set) by setting the related_name so that Manager name is now theArtworks
class Artwork(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtworks", related_query_name="theArtwork")
    #artist_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True,
                             related_name="theArtworks", related_query_name="theArtwork")
    #book_id = models.IntegerField(blank=True, null=True)
    original = models.CharField(max_length=128, blank=True, null=True)
    evidence = models.CharField(max_length=255, blank=True, null=True)
    confidence_level = models.IntegerField(blank=True, null=True)
    copyright = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    @cached_property
    def get_creator(self):
        return self.artist

    # def get_first_cover_filename(self):
    #     # can use first
    #     # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.first
    #     # should covers be theCovers?
    #     if self.covers:
    #         cover = self.covers.filter(flags__lt=256).order_by('edition__print_year')[0]
    #         # print("cover is {}".format(cover))
    #         cover_filename = cover.cover_filename
    #     return cover_filename

    class Meta:
        db_table = 'artworks'


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.country

    class Meta:
        db_table = 'countries'


class Edition(models.Model):
    edition_id = models.AutoField(primary_key=True)
    print_run_id = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True,
                             related_name="theEditions", related_query_name="theEdition")
    imprint_id = models.IntegerField(blank=True, null=True)
    genre_id = models.IntegerField(blank=True, null=True)
    format_id = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    isbn13 = models.CharField(max_length=20, blank=True, null=True)
    catalog_number = models.CharField(max_length=50, blank=True, null=True)
    print_year = models.SmallIntegerField(blank=True, null=True)
    #country_id = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True,
                                related_name="theEditions", related_query_name="theEdition")
    purchase_year = models.IntegerField(blank=True, null=True)
    purchase_price = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=3)
    currency_id = models.IntegerField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    designer = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.book.title + "," + str(self.print_year)

    class Meta:
        db_table = 'editions'


class Cover(models.Model):
    '''
    flags
    1 = Full Cover (displayed by front cover on edition page)
    2 = Author Thumbnail (used in author rotation to even out space)
    4 = variant cover for artwork
    64 = attributed to
    128 = not my cover
    >=256 = don't display
    512 = purchased
    1024 = index ?unused
    '''
    cover_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True,
                             related_name="theCovers", related_query_name="theCover")
    #artwork_id = models.IntegerField(blank=True, null=True)
    artwork = models.ForeignKey(Artwork, models.DO_NOTHING, blank=True, null=True,
                                related_name="theCovers", related_query_name="theCover")
    #edition_id = models.IntegerField(unique=True, blank=True, null=True)
    edition = models.OneToOneField(Edition, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='theCover', related_query_name="theCover")
    flags = models.IntegerField(blank=True, null=True)
    cover_filename = models.CharField(max_length=50, blank=True, null=True)
    private_notes = models.CharField(max_length=255, blank=True, null=True)
    is_variant = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cover_id}, {self.cover_filename}"

    class Meta:
        db_table = 'covers'


class PrintRun(models.Model):
    id = models.AutoField(primary_key=True)
    print_run_id = models.IntegerField()
    order = models.IntegerField()
    #edition_id = models.IntegerField(blank=True, null  =True)
    edition = models.OneToOneField(Edition, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='thePrintRun', related_query_name="thePrintRun")
    #cover_id = models.IntegerField(blank=True, null=True)
    # one cover can be used by multiple print runs
    cover = models.ForeignKey(Cover, models.DO_NOTHING, blank=True, null=True,
                              related_name="thePrintRuns", related_query_name="thePrintRun")
    print = models.CharField(max_length=255, blank=True, null=True)
    cover_price = models.CharField(max_length=255, blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    print_year = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'print_runs'
        unique_together = (('print_run_id', 'order'),)


class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'currencies'


class Format(models.Model):
    format_id = models.AutoField(primary_key=True)
    format = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.format

    class Meta:
        db_table = 'formats'


class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.genre

    class Meta:
        db_table = 'genres'


# A series is a collection, eg the Book of the New Sun,  Corgi SF Collectors Library
class Series(models.Model):
    series_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'series'


# A set is a set of covers for a series, eg
# Bruce Pennington covers for the Book of the New Sun
# Peter Andrew Jones covers for the Book of the New Sun
class Set(models.Model):
    set_id = models.AutoField(primary_key=True)
    series = models.ForeignKey(Series, models.DO_NOTHING, blank=True, null=True,
                                related_name="theSets", related_query_name="theSet")
    author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True,
                               related_name="theSets", related_query_name="theSet")
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True,
                               related_name="theSets", related_query_name="theSet")
    # series_id = models.IntegerField(blank=True, null=True)
    # author_id = models.IntegerField(blank=True, null=True)
    # artist_id = models.IntegerField(blank=True, null=True)
    imprint_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    panorama_id = models.IntegerField(blank=True, null=True)

    @cached_property
    def get_creator(self):
        Creators = collections.namedtuple('Creators', 'author artist')
        creators = Creators(author=self.author, artist=self.artist)
        return (creators)

    class Meta:
        db_table = 'sets'


# Set Exceptions are covers to exclude from a set
class SetExceptions(models.Model):
    #set_id = models.IntegerField()
    #cover_id = models.IntegerField()
    set = models.ForeignKey(Set, models.DO_NOTHING,
                            related_name="theSetExceptions", related_query_name="theSetException")
    cover = models.ForeignKey(Cover, models.DO_NOTHING,
                              related_name="theSetExceptions", related_query_name="theSetException")

    class Meta:
        db_table = 'set_exceptions'


# linking table listing all books in a series
class BookSeries(models.Model):
    # series_id = models.IntegerField()
    # book_id = models.IntegerField()
    series = models.ForeignKey(Series, models.DO_NOTHING,
                                related_name="theBooksSeries", related_query_name="theBooksSeries")
    book = models.ForeignKey(Book, models.DO_NOTHING,
                             related_name="theBooksSeries", related_query_name="theBooksSeries")
    volume = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'books_series'


class Panorama(models.Model):
    panorama_id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    #set_id = models.IntegerField(blank=True, null=True)
    #author_id = models.IntegerField(blank=True, null=True)
    #artist_id = models.IntegerField(blank=True, null=True)
    set = models.ForeignKey(Set, models.DO_NOTHING, blank=True, null=True,
                            related_name="thePanoramas", related_query_name="thePanorama")
    author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True,
                               related_name="thePanoramas", related_query_name="thePanorama")
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True,
                               related_name="thePanoramas", related_query_name="thePanorama")
    imprint_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.panorama_id}, {self.description}"

    class Meta:
        db_table = 'panoramas'


class Artbook(models.Model):
    artbook_id = models.AutoField(primary_key=True)
    # author_id = models.IntegerField(blank=True, null=True)
    # artist_id = models.IntegerField(blank=True, null=True)
    author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtbooks", related_query_name="theArtbook")
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtbooks", related_query_name="theArtbook")
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'artbooks'


class UsedAs(models.Model):
    used_as_id = models.AutoField(primary_key=True)
    used_type = models.CharField(unique=True, max_length=255, blank=False, null=False)

    def __str__(self):
        return self.used_type

    class Meta:
        db_table = 'used_as'
        # sort alphabetically in admin
        ordering = ('used_type',)

class ArtbookIndex(models.Model):
    artbook_index_id = models.AutoField(primary_key=True)
    #artbook_id = models.IntegerField(blank=True, null=True)
    artbook = models.ForeignKey(Artbook, models.DO_NOTHING,
                               related_name="theArtbookIndexes", related_query_name="theArtbookIndex")
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True,
                                  related_name="theArtbookIndexes", related_query_name="theArtbookIndex")
    page = models.IntegerField(blank=True, null=True)
    book_title = models.CharField(max_length=255, blank=True, null=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True,
                             related_name="theArtbookIndexes", related_query_name="theArtbookIndex")
    book_author_name = models.CharField(max_length=255, blank=True, null=True)
    book_author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtbookIndexes", related_query_name="theArtbookIndex")
    artwork_year = models.CharField(max_length=50, blank=True, null=True)
    cover = models.ForeignKey(Cover, models.DO_NOTHING, blank=True, null=True,
                              related_name="theArtbookIndexes", related_query_name="theArtbookIndex")
    publisher = models.CharField(max_length=255, blank=True, null=True)
    publish_year = models.CharField(max_length=50, blank=True, null=True)
    artwork_title = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    used_as = models.ForeignKey(UsedAs, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtbookIndexes", related_query_name="theArtbookIndex")
    copyright = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'artbook_index'

