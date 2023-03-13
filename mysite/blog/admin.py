from django.contrib import admin

from .models import Comment, Post, Profile


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_published']

    fieldsets = [
        (None, {'fields': ['user']}),
        ('Content', {'fields': ['content'], 'classes': ['collapse']}),
        ('Post and is_published status', {'fields': ['post', 'is_published'], 'classes': ['collapse']})
                 ]
    list_filter = ['is_published']
    search_fields = ['user', 'content']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title']

    fieldsets = [
        (None, {'fields': ['author', 'title']}),
        ('Post Text', {'fields': ['text'], 'classes': ['collapse']}),
        ('Snippet text', {'fields': ['snippet'], 'classes': ['collapse']})
                 ]
    # list_filter = [] update with adding date_field to table
    search_fields = ['author', 'title']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

    fieldsets = [
        (None, {'fields': ['user']}),
        ('Users Profile Image', {'fields': ['image']})
                 ]
    search_fields = ['user']
