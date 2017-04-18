from django.contrib import admin
from tinycontent.models import TinyContent, TinyContentFileUpload


class TinyContentAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', 'content', )


admin.site.register(TinyContent, TinyContentAdmin)


class TinyContentFileUploadAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )
    search_fields = ('name', )


admin.site.register(TinyContentFileUpload, TinyContentFileUploadAdmin)
