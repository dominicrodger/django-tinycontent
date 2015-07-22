import autoslug
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
        return TinyContent.objects.get(name=name)

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
