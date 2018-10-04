from django.db import models


class Post(models.Model):
    checkbox = models.BooleanField()
    text = models.CharField(max_length=200)
    date = models.DateField()
    foreignkey = models.ForeignKey('auth.User', models.CASCADE)

    class Meta:
        ordering = ['text']

    def __str__(self):
        return self.text
