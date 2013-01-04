from django.contrib import admin
from tinycontent.models import TinyContent


class TinyContentAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(TinyContent, TinyContentAdmin)
