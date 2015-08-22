from django.db import models


class Sentence(models.Model):
    content = models.TextField()
    who = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s (by %s)' % (self.content, self.who)
