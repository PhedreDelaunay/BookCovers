from django.contrib import admin

from bookcovers.models import Author
from bookcovers.models import Artist
from bookcovers.models import Artwork
from bookcovers.models import Book
from bookcovers.models import Cover
from bookcovers.models import Edition
from bookcovers.models import ArtbookIndex
from bookcovers.models import Artbook

# Register your models here.

# https://djangobook.com/customizing-change-lists-forms/


class CoverAdmin(admin.ModelAdmin):
    # add a search bar
    #search_fields = ['cover_filename',]

    list_display = (
        'cover_id',
        'cover_filename',
        'book',
        'artwork',
    )

    list_select_related = (
        'book',
        'artwork',
    )
    # just book
    # without book: 7.98 ms (105 queries including 102 similar and 8 duplicates )
    # with book: 1.16 ms (5 queries including 2 similar and 2 duplicates )
    # book and author
    # without artwork: 8.05 ms (105 queries including 102 similar and 6 duplicates )
    # with artwork:  1.50 ms (5 queries including 2 similar and 2 duplicates )
    # without book and artwork: 13.56 ms (205 queries including 202 similar and 12 duplicates )

    readonly_fields = (
        'edition',
    )
    # no book or edition: 50.27 ms (801 queries including 793 similar and 297 duplicates )
    # book and edition: 1.51 ms (9 queries including 2 similar and 2 duplicates )
    # edition only: 1.74 ms (9 queries )

#  https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
# https://hakibenita.com/things-you-must-know-about-django-admin-as-your-app-gets-bigger
# https://stackoverflow.com/questions/9919780/how-do-i-add-a-link-from-the-django-admin-page-of-one-object-to-the-admin-page-o
# https://avilpage.com/2017/11/django-tips-tricks-hyperlink-foreignkey-admin.html
# https://docs.djangoproject.com/en/2.2/ref/contrib/admin/#reversing-admin-urls
class AuthorAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # add a search bar
    search_fields = ['name',]


class ArtistAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # add a search bar
    search_fields = ['name',]

class EditionAdmin(admin.ModelAdmin):

    list_select_related = (
        'book',
    )
    # without book: 17.51 ms (105 queries including 102 similar and 12 duplicates )
    # with book: 1.14 ms (5 queries including 2 similar and 2 duplicates )

class ArtbookIndexAdmin(admin.ModelAdmin):
    list_display = (
        'book_title',
        'book_author_name',
    )
    # add a search bar
    search_fields = ['book_title',]

class ArtbookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'subtitle',
    )
    # add a search bar
    search_fields = ['title', ]

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Artwork)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book)
admin.site.register(Cover, CoverAdmin)
admin.site.register(Edition, EditionAdmin)
admin.site.register(ArtbookIndex, ArtbookIndexAdmin)
admin.site.register(Artbook, ArtbookAdmin)