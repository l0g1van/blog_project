from django.contrib import admin

from .models import Profile, Comment, Post

admin.site.register(Profile)
admin.site.register(Post)

admin.site.register(Comment)
