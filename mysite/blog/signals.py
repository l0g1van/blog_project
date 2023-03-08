from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Post
from .task import post_created_email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Post)
def post_created_message(instance, created, *args, **kwargs):
    if created:
        post_created_email.delay(f'User {instance.author.username}`ve just created a new post, named "{instance.title}"')
