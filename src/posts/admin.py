from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('topic', 'user', 'created_on', 'active', 'body')
    list_filter = ('active', 'created_on')
    ordering = ['topic']
    search_fields = ('user', 'body')
    actions = ['approve_comments']


    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = "Approve these comments"


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'likes', 'dislikes', 'created_on']
    list_filter = ['likes', 'dislikes', 'created_on']
    search_fields = ['user', 'topic']


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('id', 'user', 'title', 'slug', 'publish_date', 'image')


admin.site.register(Post, PostAdmin)
