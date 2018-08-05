# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class ArtbookIndex(models.Model):
    artbook_index_id = models.AutoField(primary_key=True)
    artbook_id = models.IntegerField(blank=True, null=True)
    page = models.IntegerField(blank=True, null=True)
    book_title = models.CharField(max_length=255, blank=True, null=True)
    book_author = models.CharField(max_length=255, blank=True, null=True)
    cover_year = models.CharField(max_length=50, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artbook_index'


class Artbooks(models.Model):
    artbook_id = models.AutoField(primary_key=True)
    author_id = models.IntegerField(blank=True, null=True)
    artist_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artbooks'


class ArtistAkas(models.Model):
    artist_aka_id = models.IntegerField()
    artist_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'artist_akas'


class Artists(models.Model):
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

    class Meta:
        managed = False
        db_table = 'artists'


class Artworks(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    artist_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    book_id = models.IntegerField(blank=True, null=True)
    original = models.CharField(max_length=128, blank=True, null=True)
    evidence = models.CharField(max_length=255, blank=True, null=True)
    confidence_level = models.IntegerField(blank=True, null=True)
    copyright = models.CharField(max_length=128, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'artworks'


class AuthorAkas(models.Model):
    author_aka_id = models.IntegerField()
    author_id = models.IntegerField()
    real_name = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'author_akas'


class Authors(models.Model):
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

    class Meta:
        managed = False
        db_table = 'authors'

# https://docs.djangoproject.com/en/2.0/topics/db/queries/#backwards-related-objects
# if a model has a ForeignKey, instances of the foreign-key model will have access to a Manager 
# that returns all instances of the first model. 
# By default, this Manager is named FOO_set, where FOO is the source model name, lowercased
# You can override the FOO_set name by setting the related_name parameter in the ForeignKey definition
class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Authors, models.DO_NOTHING, blank=True, null=True, related_name="books", related_query_name="book")
    title = models.CharField(unique=True, max_length=50, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    copyright_year = models.IntegerField(blank=True, null=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    quick_notes = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class BooksSeries(models.Model):
    series_id = models.IntegerField()
    book_id = models.IntegerField()
    volume = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books_series'


class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'

class Editions(models.Model):
    edition_id = models.AutoField(primary_key=True)
    print_run_id = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True, related_name="editions", related_query_name="edition")
    imprint_id = models.IntegerField(blank=True, null=True)
    genre_id = models.IntegerField(blank=True, null=True)
    format_id = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    isbn13 = models.CharField(max_length=20, blank=True, null=True)
    catalog_number = models.CharField(max_length=50, blank=True, null=True)
    print_year = models.SmallIntegerField(blank=True, null=True)
    country_id = models.IntegerField(blank=True, null=True)
    purchase_year = models.IntegerField(blank=True, null=True)
    purchase_price = models.FloatField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    designer = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editions'

class Covers(models.Model):
    cover_id = models.AutoField(primary_key=True)
    book_id = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True, related_name="covers", related_query_name="cover")
    artwork_id = models.IntegerField(blank=True, null=True)
    #edition_id = models.IntegerField(unique=True, blank=True, null=True)
    edition = models.OneToOneField(Editions, on_delete=models.DO_NOTHING, blank=True, null=True)

    flags = models.IntegerField(blank=True, null=True)
    cover_filename = models.CharField(max_length=50, blank=True, null=True)
    private_notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covers'


class Currencies(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'currencies'


class Formats(models.Model):
    format_id = models.AutoField(primary_key=True)
    format = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'formats'


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genres'


class ImprintNames(models.Model):
    imprint_name_id = models.AutoField(primary_key=True)
    imprint_name = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imprint_names'


class Imprints(models.Model):
    imprint_id = models.AutoField(primary_key=True)
    imprint_name_id = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    imprint_alternate_name = models.CharField(max_length=50, blank=True, null=True)
    imprint_description = models.CharField(max_length=255, blank=True, null=True)
    logo_id = models.IntegerField(blank=True, null=True)
    publisher_relationship = models.CharField(max_length=50, blank=True, null=True)
    publisher_id = models.IntegerField(blank=True, null=True)
    year_founded = models.IntegerField(blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imprints'


class Panoramas(models.Model):
    panorama_id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=50, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    set_id = models.IntegerField(blank=True, null=True)
    author_id = models.IntegerField(blank=True, null=True)
    artist_id = models.IntegerField(blank=True, null=True)
    imprint_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'panoramas'


class PrintRuns(models.Model):
    print_run_id = models.IntegerField()
    order = models.IntegerField()
    edition_id = models.IntegerField(blank=True, null=True)
    cover_id = models.IntegerField(blank=True, null=True)
    print = models.CharField(max_length=255, blank=True, null=True)
    cover_price = models.CharField(max_length=255, blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    print_year = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'print_runs'
        unique_together = (('print_run_id', 'order'),)


class Series(models.Model):
    series_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series'


class SetExceptions(models.Model):
    set_id = models.IntegerField()
    cover_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'set_exceptions'


class Sets(models.Model):
    set_id = models.AutoField(primary_key=True)
    series_id = models.IntegerField(blank=True, null=True)
    author_id = models.IntegerField(blank=True, null=True)
    artist_id = models.IntegerField(blank=True, null=True)
    imprint_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    panorama_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sets'

