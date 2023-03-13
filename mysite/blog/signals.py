from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment, Post, Profile
from .task import comment_created_email, post_created_email


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Post)
def post_created_message(instance, created, *args, **kwargs):
    if created:
        post_created_email.delay(f'User {instance.author.username}`ve just '
                                 f'created a new post, named "{instance.title}"')


@receiver(post_save, sender=Comment)
def comment_created_message(instance, created, *args, **kwargs):
    if created:
        comment_created_email.delay(f'There is a new comment under '
                                    f'your {instance.post.title} post, '
                                    f'here is link to that post: http://127.0.0.1:8000/post/{instance.post.pk}',
                                    instance.post.author.email)
