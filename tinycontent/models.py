import base64
import autoslug
from django.core.cache import cache
from django.db import models
from tinycontent.conf import get_filter_list


class TinyContent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.name

    def rendered_content(self):
        filters = get_filter_list()

        content = self.content

        for filter in filters:
            content = filter(content)

        return content

    @staticmethod
    def get_content_by_name(name):
        cache_key = TinyContent.get_cache_key(name)
        obj = cache.get(cache_key)

        if obj is None:
            obj = TinyContent.objects.get(name=name)
            cache.set(cache_key, obj)

        return obj

    @staticmethod
    def get_cache_key(name):
        return 'tinycontent_%s' % base64.b64encode(bytes(name, 'utf-8'))

    def delete(self, *args, **kwargs):
        cache.delete(TinyContent.get_cache_key(self.name))
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        cache.delete(TinyContent.get_cache_key(self.name))
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Content block'


class TinyContentFileUpload(models.Model):
    name = models.CharField(
        max_length=60,
        help_text='The name of the file.'
    )
    slug = autoslug.AutoSlugField(populate_from='name', unique=True)
    file = models.FileField(upload_to='tinycontent/uploads')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'File upload'
        ordering = ('-created', )
