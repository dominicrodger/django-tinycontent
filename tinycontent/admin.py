from django.contrib import admin
from tinycontent.models import TinyContent


class TinyContentAdmin(admin.ModelAdmin):
    list_display = ('label', )

admin.site.register(TinyContent, TinyContentAdmin)
