from django.conf import settings
from django.db import models


class Post(models.Model):
    VINYL = 'vinyl'
    CD = 'cd'
    MP3 = 'mp3'
    VHS = 'vhs'
    DVD = 'dvd'
    BLURAY = 'blu-ray'
    MEDIA_CHOICES = (
        ('Audio', (
            (VINYL, 'Vinyl'),
            (CD, 'CD'),
            (MP3, 'MP3')
            )
         ),
        ('Video', (
            (VHS, 'VHS tape'),
            (DVD, 'DVD'),
            (BLURAY, 'Blu-ray')
            )
         ),
    )

    checkbox = models.BooleanField()
    text = models.CharField(max_length=200)
    date = models.DateField()
    media = models.CharField(max_length=12,
                             choices=MEDIA_CHOICES)
    foreignkey = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)

    class Meta:
        ordering = ['text']

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("blog:post_update",
                       kwargs={'pk': self.pk})
