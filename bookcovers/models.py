# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# https://docs.djangoproject.com/en/2.0/intro/tutorial02/
# It’s important to add __str__() methods to your models, 
# not only for your own convenience when dealing with the interactive prompt, 
# but also because objects’ representations are used throughout Django’s automatically-generated admin.


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

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'artists'


class ArtistAkas(models.Model):
    artist_aka_id = models.IntegerField()
    artist = models.ForeignKey(Artists, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtist_akas", related_query_name="theArtist_aka")
    #artist = models.IntegerField(db_column='artist_id')

    def __str__(self):
        return self.artists.name

    class Meta:
        db_table = 'artist_akas'

#class AuhtorManager(models.Manager):
#    def get_by_natural_key(self, fullname):
#        return self.get(fullname=fullname)

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

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'authors'

class AuthorAkas(models.Model):
    # pk=id is implied
    author_aka_id = models.IntegerField()
    author = models.ForeignKey(Authors, models.DO_NOTHING, blank=True, null=True,
                               related_name="theAuthor_akas", related_query_name="theAuthor_aka")
    real_name = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.authors.name

    class Meta:
        db_table = 'author_akas'

# https://docs.djangoproject.com/en/2.0/topics/db/queries/#backwards-related-objects
# if a model has a ForeignKey, instances of the foreign-key model will have access to a Manager 
# that returns all instances of the first model. 
# By default, this Manager is named FOO_set, where FOO is the source model name, lowercased
# You can override the FOO_set name by setting the related_name parameter in the ForeignKey definition
# related_query_name creates a relation from the related object back to this one. This allows querying and filtering from the related object.
class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Authors, models.DO_NOTHING, blank=True, null=True,
                               related_name="theBooks", related_query_name="theBook")
    title = models.CharField(unique=True, max_length=50, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    copyright_year = models.IntegerField(blank=True, null=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    quick_notes = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'books'


# https://docs.djangoproject.com/en/2.0/topics/db/queries/#backwards-related-objects
# override the FOO_set name (artworks_set) by setting the related_name so that Manager name is now theArtworks
class Artworks(models.Model):
    artwork_id = models.AutoField(primary_key=True)
    artist = models.ForeignKey(Artists, models.DO_NOTHING, blank=True, null=True,
                               related_name="theArtworks", related_query_name="theArtwork")
    #artist_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True,
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

    def get_first_cover_filename(self):
        if self.covers:
            cover = self.covers.filter(flags__lt=256).order_by('edition__print_year')[0]
            # print("cover is {}".format(cover))
            cover_filename = cover.cover_filename
        return cover_filename

    class Meta:
        db_table = 'artworks'

class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.country

    class Meta:
        db_table = 'countries'

class Editions(models.Model):
    edition_id = models.AutoField(primary_key=True)
    print_run_id = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True,
                             related_name="theEditions", related_query_name="theEdition")
    imprint_id = models.IntegerField(blank=True, null=True)
    genre_id = models.IntegerField(blank=True, null=True)
    format_id = models.IntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    isbn13 = models.CharField(max_length=20, blank=True, null=True)
    catalog_number = models.CharField(max_length=50, blank=True, null=True)
    print_year = models.SmallIntegerField(blank=True, null=True)
    #country_id = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING, blank=True, null=True,
                                related_name="theEditions", related_query_name="theEdition")
    purchase_year = models.IntegerField(blank=True, null=True)
    purchase_price = models.FloatField(blank=True, null=True)
    currency_id = models.IntegerField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    designer = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.book.title + "," + str(self.print_year)

    class Meta:
        db_table = 'editions'

class Covers(models.Model):
    cover_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True,
                             related_name="theCovers", related_query_name="theCover")
    #artwork_id = models.IntegerField(blank=True, null=True)
    artwork = models.ForeignKey(Artworks, models.DO_NOTHING, blank=True, null=True,
                                related_name="theCovers", related_query_name="theCover")
    #edition_id = models.IntegerField(unique=True, blank=True, null=True)
    edition = models.OneToOneField(Editions, on_delete=models.DO_NOTHING, blank=True, null=True,
                                   related_name='theCover', related_query_name="theCover")
    flags = models.IntegerField(blank=True, null=True)
    cover_filename = models.CharField(max_length=50, blank=True, null=True)
    private_notes = models.CharField(max_length=255, blank=True, null=True)
    is_variant = models.BooleanField(default=False)

    def __str__(self):
        return self.cover_filename

    class Meta:
        db_table = 'covers'


class Currencies(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'currencies'


class Formats(models.Model):
    format_id = models.AutoField(primary_key=True)
    format = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.format

    class Meta:
        db_table = 'formats'


class Genres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.genre

    class Meta:
        db_table = 'genres'


