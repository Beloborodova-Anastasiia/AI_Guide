from django.contrib import admin

from .models import Attraction


class AttractiontAdmin(admin.ModelAdmin):
    list_display = ('pk', 'object_name', 'location',)
    list_filter = ('object_name',)
    empty_value_display = '-empty-'
    search_fields = ('object_name',)
    sortable_by = ('object_name',)


admin.site.register(Attraction, AttractiontAdmin)
