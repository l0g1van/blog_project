from datetime import datetime

from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    # text = models.TextField()
    text = RichTextField(blank=True, null=True)
    title = models.CharField(max_length=255)
    snippet = models.CharField(max_length=200, default='Click Link Above To Get More Info')
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} {self.author}'

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))

    def comments(self):
        return self.comment_set.all()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile/default.jpg', upload_to='profile_page', validators=[
        FileExtensionValidator(['png', 'jpg'])
    ])

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.CharField(max_length=150)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    is_published = models.BooleanField(default=True)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
