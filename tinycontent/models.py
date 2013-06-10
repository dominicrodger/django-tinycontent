from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from tinycontent.utils import import_from_setting


@python_2_unicode_compatible
class TinyContent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    content = models.TextField()

    def __str__(self):
        return self.name

    def rendered_content(self):
        try:
            func = import_from_setting('TINYCONTENT_FILTER')
            return func(self.content)
        except AttributeError:
            return self.content

    class Meta:
        verbose_name = 'Content block'
