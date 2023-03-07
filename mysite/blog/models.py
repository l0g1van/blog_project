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

    def __str__(self):
        return self.title, str(self.author)

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile/default.jpg', upload_to='profile_page', validators=[
        FileExtensionValidator(['png', 'jpg'])
    ])

    def __str__(self):
        return self.user.username
