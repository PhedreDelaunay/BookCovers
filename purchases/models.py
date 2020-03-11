from django.db import models

# Create your models here.
from bookcovers.models import Author
from bookcovers.models import Artist
from bookcovers.models import Book
from bookcovers.models import Artwork
from bookcovers.models import Edition
from bookcovers.models import Cover
from bookcovers.models import BookSeries
from bookcovers.models import Set

class Owned(models.Model):
    owned_id = models.AutoField(primary_key=True)
    purchase_date = models.CharField(max_length=10, blank=True, null=True)
    title = models.CharField(max_length=100)
    author_name = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255, blank=True, null=True)
    publisher_year = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Author, models.DO_NOTHING, blank=True, null=True)
    artist = models.ForeignKey(Artist, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(Book, models.DO_NOTHING, blank=True, null=True)
    artwork = models.ForeignKey(Artwork, models.DO_NOTHING, blank=True, null=True)
    edition = models.ForeignKey(Edition, on_delete=models.DO_NOTHING, blank=True, null=True)
    cover = models.ForeignKey(Cover, models.DO_NOTHING, blank=True, null=True)
    print_run = models.CharField(max_length=25, blank=True, null=True)
    series = models.CharField(max_length=255, blank=True, null=True)
    book_series = models.ForeignKey(BookSeries, models.DO_NOTHING, blank=True, null=True)
    set = models.ForeignKey(Set, models.DO_NOTHING, blank=True, null=True)
    imprint = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=25, blank=True, null=True)
    isfdb = models.CharField(max_length=50, blank=True, null=True)
    cost = models.CharField(max_length=25, blank=True, null=True)
    total_cost = models.CharField(max_length=50, blank=True, null=True)
    purchased_from = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.author_name}: {self.title}"

    class Meta:
        db_table = 'purchases_owned'