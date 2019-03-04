from django.contrib import admin

from bookcovers.models import Author
from bookcovers.models import Artists

# Register your models here.

# https://djangobook.com/customizing-change-lists-forms/

class AuthorAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # add a search bar
    search_fields = ['name',]

admin.site.register(Author, AuthorAdmin)

class ArtistAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # add a search bar
    search_fields = ['name',]

admin.site.register(Artists, ArtistAdmin)