from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User)
    theme = models.CharField(max_length=100)

    def __unicode__(self):
        return (u'user: {} ({}), theme: {}'
                .format(self.user, self.user.email, self.theme))


class Reply(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    tatoe = models.CharField(max_length=100)

    def __unicode__(self):
        return (u'user: {} ({}), post: {}, tatoe: {}'
                .format(self.user, self.user.email, self.post, self.tatoe))
