from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    text = models.TextField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title, str(self.author)

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))
