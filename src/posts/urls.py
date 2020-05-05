from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('posts', views.allPosts, name="all-posts"),
    path('posts-new', views.createPost, name="new-post"),
    path('posts/<str:slug>', views.showPost, name="show-post"),
    path('posts/<str:slug>/edit', views.updatePost, name="edit-post"),
    path('posts/<str:slug>/delete', views.destroyPost, name="delete-post"),
    path('posts/<str:slug>/like', views.likePost, name="like-post"),
    path('posts/<str:slug>/dislike', views.disLikePost, name="dislike_post"),
]