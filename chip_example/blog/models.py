from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', models.CASCADE)
    publish_datetime = models.DateTimeField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
