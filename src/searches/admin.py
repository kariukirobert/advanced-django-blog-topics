from django.contrib import admin
from .models import SearchQuery


class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('user', 'query', 'timestamp')


admin.site.register(SearchQuery, SearchQueryAdmin)