from django.contrib import admin

from purchases.models import Owned

# Register your models here.

class OwnedAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # add a search bar
    ordering = ('author_name',)
    search_fields = ['author_name','title',]

admin.site.register(Owned, OwnedAdmin)