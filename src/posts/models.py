from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone


User = settings.AUTH_USER_MODEL


class PostQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(publish_date__lte=now)
    
    def search(self, query):
        lookup = (
            Q(title__icontains=query) |
            Q(slug__icontains=query) |
            Q(content__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(user__username__icontains=query)
        )
        return self.filter(lookup)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()
    
    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query)

class Post(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=191)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    image = models.FileField(upload_to='images/')
    publish_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = PostManager()

    class Meta:
        ordering = ['-publish_date', '-updated', '-timestamp']

    def get_absolute_url(self):
        return f"/posts/{self.slug}"
    
    def get_edit_url(self):
        return f"/posts/{self.slug}/edit"
    
    def get_delete_url(self):
        return f"/posts/{self.slug}/delete"

    def like_post_url(self):
        return f"/posts/{self.slug}/like"
    
    def dislike_post_url(self):
        return f"/posts/{self.slug}/dislike"

class Comment(models.Model):
    topic = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='comments')
    # topic = models.IntegerField()
    body = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)
    
class Like(models.Model):
    posts = models.ManyToManyField(Post, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    likes = models.IntegerField(null=True, blank=True)
    dislikes = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)