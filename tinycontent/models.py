import autoslug
from django.core.cache import cache
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from tinycontent.conf import get_filter_list


@python_2_unicode_compatible
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
        return 'tinycontent_%s' % name

    def delete(self, *args, **kwargs):
        cache.delete(TinyContent.get_cache_key(self.name))
        return super(TinyContent, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        cache.delete(TinyContent.get_cache_key(self.name))
        return super(TinyContent, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Content block'


@python_2_unicode_compatible
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
