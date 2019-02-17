from django.contrib import admin

from bookcovers.models import Authors

# Register your models here.

# https://djangobook.com/customizing-change-lists-forms/

class AuthorAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # add a search bar
    search_fields = ['name',]

admin.site.register(Authors, AuthorAdmin)