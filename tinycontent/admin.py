from django.contrib import admin
from tinycontent.models import TinyContent


class TinyContentAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', 'content', )

admin.site.register(TinyContent, TinyContentAdmin)
