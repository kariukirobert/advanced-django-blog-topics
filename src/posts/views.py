from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import Post, Like
from .post_form import PostModelForm
from .comment_form import CommentForm


def index(request):
    posts = Post.objects.all().published()[:6]
    return render(request, 'index.html', {'posts': posts})


def allPosts(request):
    posts = Post.objects.all().select_related() #.published()
    # likes = posts.likes #.filter(likes=1)
    # if request.user.is_authenticated:
        # qs_query = Post.objects.filter(user=request.user)
        # posts = (posts | qs_query).distinct()
    return render(request, 'post/all.html', {'posts': posts})


@login_required(login_url='/login')
def createPost(request):
    form = PostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # obj = form.cleaned_data
        # obj['user'] = request.user
        # Post.objects.create(**obj)
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()

        form = PostModelForm()
        return HttpResponseRedirect("/posts")
    
    return render(request, 'post/create_post.html', { 'title': "Create a New Post", 'form': form })

def showPost(request, slug):
    obj = Post.objects.filter(slug=slug)
    obj = get_object_or_404(Post, slug=slug)
    comments = obj.comments.filter(active=True)
    # obj.likes_count = obj.likes.count()
    # obj.dislikes_count = obj.likes.count()
    obj.likes_count = obj.likes.filter(likes=1).count()
    obj.dislikes_count = obj.likes.filter(dislikes=1).count()
    
    # new_comment = None
    #Comment Posted
    comment_form = CommentForm(request.POST or None )
    if comment_form.is_valid():
        #create comment object but don't save to save to db yet
        comment_form = comment_form.save(commit=False)
        #assign the current post to the comment
        comment_form.topic = obj
        comment_form.user = request.user
        #save the comment to db
        comment_form.save()
        comment_form = CommentForm()
    
    context = {'post': obj, 'comments': comments, 'comment_form': comment_form }

    return render(request, 'post/single_post.html', context)


def updatePost(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    form = PostModelForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = PostModelForm()
        return redirect('/posts')
    return render(request, 'post/update.html', { 'post': obj, 'form': form })


def destroyPost(request, slug):
    obj = get_object_or_404(Post, slug=slug)
    if request.method == 'POST' :
        obj.delete()
        return redirect('/posts')
    return render(request, 'post/delete.html', {'title': obj.title})

def likePost(request, slug):
    topic = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        filter_likes = topic.likes.filter(user=request.user)
        if filter_likes.count() > 0:
            for item in filter_likes:
                if item.likes:
                    item.delete()
                else:
                    item.dislikes = None
                    item.likes = 1
                    item.save()
        else:
            like = Like.objects.create(user=request.user, likes=1)
            topic.likes.add(like)
    return HttpResponseRedirect(f"/posts/{slug}")

def disLikePost(request, slug):
    topic = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        filter_dislikes = topic.likes.filter(user=request.user)
        if filter_dislikes.count() > 0:
            for item in filter_dislikes:
                if item.dislikes:
                    item.delete()
                else:
                    item.likes = None
                    item.dislikes = 1
                    item.save()
                    # print(item)
        else:
            dislike = Like.objects.create(user=request.user, dislikes=1)
            topic.likes.add(dislike)
    return HttpResponseRedirect(f"/posts/{slug}")