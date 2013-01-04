from django.db import models


class TinyContent(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    content = models.TextField()

    def __unicode__(self):
        return self.name
