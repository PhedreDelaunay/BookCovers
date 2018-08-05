# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Artwork(models.Model):
    artwork_id = models.AutoField(db_column='ArtWorkID', primary_key=True)  # Field name made lowercase.
    artist_id = models.ForeignKey('Artist', models.DO_NOTHING, db_column='ArtistID', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=255, blank=True, null=True)  # Field name made lowercase.
    book_id = models.ForeignKey('Book', models.DO_NOTHING, db_column='BookID', blank=True, null=True)  # Field name made lowercase.
    art_type_id = models.IntegerField(db_column='ArtTypeID', blank=True, null=True)  # Field name made lowercase.
    original = models.CharField(db_column='Original', max_length=128, blank=True, null=True)  # Field name made lowercase.
    evidence = models.CharField(db_column='Evidence', max_length=255, blank=True, null=True)  # Field name made lowercase.
    confidence_level = models.IntegerField(db_column='ConfidenceLevel', blank=True, null=True)  # Field name made lowercase.
    copyright = models.CharField(db_column='Copyright', max_length=128, blank=True, null=True)  # Field name made lowercase.
    description2 = models.CharField(db_column='Description2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ArtWork'


class Artist(models.Model):
    artist_id = models.AutoField(db_column='ArtistID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cover_filepath = models.CharField(db_column='CoverFilepath', max_length=128, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=128, blank=True, null=True)  # Field name made lowercase.
    dob_day = models.PositiveIntegerField(db_column='DoBDay', blank=True, null=True)  # Field name made lowercase.
    dob_month = models.PositiveIntegerField(db_column='DoBMonth', blank=True, null=True)  # Field name made lowercase.
    dob_year = models.SmallIntegerField(db_column='DoBYear', blank=True, null=True)  # Field name made lowercase.
    dod_day = models.PositiveIntegerField(db_column='DoDDay', blank=True, null=True)  # Field name made lowercase.
    dod_month = models.PositiveIntegerField(db_column='DoDMonth', blank=True, null=True)  # Field name made lowercase.
    dod_year = models.SmallIntegerField(db_column='DoDYear', blank=True, null=True)  # Field name made lowercase.
    birthplace = models.CharField(db_column='Birthplace', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Artist'


class ArtistAka(models.Model):
    artist_id = models.IntegerField(db_column='ArtistID', primary_key=True)  # Field name made lowercase.
    artist_aka_id = models.ForeignKey(Artist, models.DO_NOTHING, db_column='ArtistAKAID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Artist_AKA'
        unique_together = (('artist_id', 'artist_aka_id'),)


class Author(models.Model):
    author_id = models.AutoField(db_column='AuthorID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    fullname = models.CharField(db_column='FullName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=128, blank=True, null=True)  # Field name made lowercase.
    dob_day = models.PositiveIntegerField(db_column='DoBDay', blank=True, null=True)  # Field name made lowercase.
    dob_month = models.PositiveIntegerField(db_column='DoBMonth', blank=True, null=True)  # Field name made lowercase.
    dob_year = models.SmallIntegerField(db_column='DoBYear', blank=True, null=True)  # Field name made lowercase.
    dod_day = models.PositiveIntegerField(db_column='DoDDay', blank=True, null=True)  # Field name made lowercase.
    dod_month = models.PositiveIntegerField(db_column='DoDMonth', blank=True, null=True)  # Field name made lowercase.
    dod_year = models.SmallIntegerField(db_column='DoDYear', blank=True, null=True)  # Field name made lowercase.
    birthplace = models.CharField(db_column='Birthplace', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'Author'


class Authorwebsites(models.Model):
    author_id = models.ForeignKey(Author, models.DO_NOTHING, db_column='AuthorID', blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AuthorWebsites'


class AuthorAka(models.Model):
    author_id = models.ForeignKey(Author, models.DO_NOTHING, db_column='AuthorID', primary_key=True)  # Field name made lowercase.
    author_aka_id = models.IntegerField(db_column='AuthorAKAID')  # Field name made lowercase.
    realname = models.IntegerField(db_column='RealName', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Author_AKA'
        unique_together = (('author_id', 'author_aka_id'),)


class Book(models.Model):
    book_id = models.AutoField(db_column='BookID', primary_key=True)  # Field name made lowercase.
    author_id = models.ForeignKey(Author, models.DO_NOTHING, db_column='AuthorID', blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    subtitle = models.CharField(db_column='Subtitle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    copyright_year = models.IntegerField(db_column='CopyrightYear', blank=True, null=True)  # Field name made lowercase.
    copyright = models.CharField(db_column='Copyright', max_length=255, blank=True, null=True)  # Field name made lowercase.
    synopsis = models.TextField(db_column='Synopsis', blank=True, null=True)  # Field name made lowercase.
    quick_notes = models.CharField(db_column='QuickNotes', max_length=128, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Book'


class Bookartworkquote(models.Model):
    artwork_id = models.ForeignKey(Artwork, models.DO_NOTHING, db_column='ArtWorkID', blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    quote = models.TextField(db_column='Quote', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookArtWorkQuote'


class Bookcover(models.Model):
    book_cover_id = models.AutoField(db_column='BookCoverID', primary_key=True)  # Field name made lowercase.
    book_id = models.ForeignKey(Book, models.DO_NOTHING, db_column='BookID', blank=True, null=True)  # Field name made lowercase.
    artwork_id = models.IntegerField(db_column='ArtWorkID', blank=True, null=True)  # Field name made lowercase.
    book_edition_id = models.IntegerField(db_column='BookEditionID', unique=True, blank=True, null=True)  # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags', blank=True, null=True)  # Field name made lowercase.
    cover_filename = models.CharField(db_column='CoverFilename', max_length=50, blank=True, null=True)  # Field name made lowercase.
    private_notes = models.CharField(db_column='PrivateNotes', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookCover'


class Bookedition(models.Model):
    book_edition_id = models.AutoField(db_column='BookEditionID', primary_key=True)  # Field name made lowercase.
    book_printrun_id = models.IntegerField(db_column='BookPrintRunID', blank=True, null=True)  # Field name made lowercase.
    book_id = models.ForeignKey(Book, models.DO_NOTHING, db_column='BookID', blank=True, null=True)  # Field name made lowercase.
    book_imprint_id = models.IntegerField(db_column='BookImprintID', blank=True, null=True)  # Field name made lowercase.
    genre_id = models.IntegerField(db_column='GenreID', blank=True, null=True)  # Field name made lowercase.
    format_id = models.IntegerField(db_column='FormatID', blank=True, null=True)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    isbn13 = models.CharField(db_column='ISBN13', max_length=20, blank=True, null=True)  # Field name made lowercase.
    other_book_number = models.CharField(db_column='OtherBookNumber', max_length=50, blank=True, null=True)  # Field name made lowercase.
    print_year = models.SmallIntegerField(db_column='PrintYear', blank=True, null=True)  # Field name made lowercase.
    country_id = models.IntegerField(db_column='CountryID', blank=True, null=True)  # Field name made lowercase.
    purchase_year = models.IntegerField(db_column='PurchaseYear', blank=True, null=True)  # Field name made lowercase.
    purchase_price = models.FloatField(db_column='PurchasePrice', blank=True, null=True)  # Field name made lowercase.
    currency_id = models.IntegerField(db_column='CurrencyID', blank=True, null=True)  # Field name made lowercase.
    flags = models.IntegerField(db_column='Flags', blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.
    designer = models.CharField(db_column='Designer', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookEdition'


class Bookformat(models.Model):
    format_id = models.AutoField(db_column='FormatID', primary_key=True)  # Field name made lowercase.
    format = models.CharField(db_column='Format', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookFormat'


class Bookgenre(models.Model):
    genre_id = models.AutoField(db_column='GenreID', primary_key=True)  # Field name made lowercase.
    genre_name = models.CharField(db_column='GenreName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookGenre'


class Bookpanorama(models.Model):
    book_panorama_id = models.AutoField(db_column='BookPanoramaID', primary_key=True)  # Field name made lowercase.
    panorama_filename = models.CharField(db_column='PanoramaFilename', max_length=50, blank=True, null=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order', blank=True, null=True)  # Field name made lowercase.
    bookset_id = models.IntegerField(db_column='BookSetID', blank=True, null=True)  # Field name made lowercase.
    author_id = models.IntegerField(db_column='AuthorID', blank=True, null=True)  # Field name made lowercase.
    artist_id = models.IntegerField(db_column='ArtistID', blank=True, null=True)  # Field name made lowercase.
    imprint_id = models.IntegerField(db_column='ImprintID', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookPanorama'


class Bookprintrun(models.Model):
    book_printrun_id = models.IntegerField(db_column='BookPrintRunID', primary_key=True)  # Field name made lowercase.
    order = models.IntegerField(db_column='Order')  # Field name made lowercase.
    book_edition_id = models.IntegerField(db_column='BookEditionID', blank=True, null=True)  # Field name made lowercase.
    book_cover_id = models.IntegerField(db_column='BookCoverID', blank=True, null=True)  # Field name made lowercase.
    print = models.CharField(db_column='Print', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cover_price = models.CharField(db_column='CoverPrice', max_length=255, blank=True, null=True)  # Field name made lowercase.
    num_pages = models.IntegerField(db_column='NumPages', blank=True, null=True)  # Field name made lowercase.
    print_year = models.CharField(db_column='PrintYear', max_length=255, blank=True, null=True)  # Field name made lowercase.
    notes = models.CharField(db_column='Notes', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookPrintRun'
        unique_together = (('book_printrun_id', 'order'),)


class Bookseries(models.Model):
    book_series_id = models.AutoField(db_column='BookSeriesID', primary_key=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=50, blank=True, null=True)  # Field name made lowercase.
    synopsis = models.TextField(db_column='Synopsis', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookSeries'


class BookseriesLink(models.Model):
    book_series_id = models.ForeignKey(Bookseries, models.DO_NOTHING, db_column='BookSeriesID', primary_key=True)  # Field name made lowercase.
    book_id = models.IntegerField(db_column='BookID')  # Field name made lowercase.
    volume = models.IntegerField(db_column='Volume', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookSeries_Link'
        unique_together = (('book_series_id', 'book_id'),)


class Bookset(models.Model):
    book_set_id = models.AutoField(db_column='BookSetID', primary_key=True)  # Field name made lowercase.
    book_series_id = models.IntegerField(db_column='BookSeriesID', blank=True, null=True)  # Field name made lowercase.
    author_id = models.IntegerField(db_column='AuthorID', blank=True, null=True)  # Field name made lowercase.
    artist_id = models.IntegerField(db_column='ArtistID', blank=True, null=True)  # Field name made lowercase.
    imprint_id = models.IntegerField(db_column='ImprintID', blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=50, blank=True, null=True)  # Field name made lowercase.
    book_panorama_id = models.IntegerField(db_column='BookPanoramaID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookSet'


class BooksetExceptions(models.Model):
    book_set_id = models.ForeignKey(Bookset, models.DO_NOTHING, db_column='BookSetID', primary_key=True)  # Field name made lowercase.
    book_cover_id = models.IntegerField(db_column='BookCoverID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BookSet_exceptions'
        unique_together = (('book_set_id', 'book_cover_id'),)


class Country(models.Model):
    country_id = models.AutoField(db_column='CountryID', primary_key=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, blank=True, null=True)  # Field name made lowercase.
    display_order = models.IntegerField(db_column='DisplayOrder', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Country'


class Criteriaheadings(models.Model):
    criteria_heading = models.CharField(db_column='CRITERIA_HEADING', max_length=50, blank=True, null=True)  # Field name made lowercase.
    criteria_order = models.IntegerField(db_column='CRITERIA_ORDER', blank=True, null=True)  # Field name made lowercase.
    option_type = models.IntegerField(db_column='OPTION_TYPE', blank=True, null=True)  # Field name made lowercase.
    criteria_option_table = models.CharField(db_column='CRITERIA_OPTION_TABLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    num_criteria_fields = models.IntegerField(db_column='NUM_CRITERIA_FIELDS', blank=True, null=True)  # Field name made lowercase.
    criteria_option_field = models.CharField(db_column='CRITERIA_OPTION_FIELD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    criteria_where_clause = models.CharField(db_column='CriteriaWhereClause', max_length=50, blank=True, null=True)  # Field name made lowercase.
    search_select_clause = models.CharField(db_column='SearchSelectClause', max_length=128, blank=True, null=True)  # Field name made lowercase.
    search_option_table = models.CharField(db_column='SEARCH_OPTION_TABLE', max_length=50, blank=True, null=True)  # Field name made lowercase.
    num_search_fields = models.IntegerField(db_column='NUM_SEARCH_FIELDS', blank=True, null=True)  # Field name made lowercase.
    search_option_field = models.CharField(db_column='SEARCH_OPTION_FIELD', max_length=50, blank=True, null=True)  # Field name made lowercase.
    search_where_clause = models.CharField(db_column='SearchWhereClause', max_length=128, blank=True, null=True)  # Field name made lowercase.
    values_flag = models.IntegerField(db_column='VALUES_FLAG', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CriteriaHeadings'


class Currencys(models.Model):
    currency_id = models.AutoField(db_column='CurrencyID', primary_key=True)  # Field name made lowercase.
    currency_name = models.CharField(db_column='CurrencyName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, blank=True, null=True)  # Field name made lowercase.
    notes = models.TextField(db_column='Notes', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Currencys'
