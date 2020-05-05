from django.shortcuts import render
from .models import SearchQuery
from posts.models import Post

def searchPost(request):
    query = request.GET.get('q', None)
    # query = request.POST.get('q', None)
    # query = query.cleaned_data
    user = None
    if request.user.is_authenticated:
        user = request.user
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        qs = Post.objects.search(query=query)
    return render(request, 'searches/view.html', { 'query': query, 'posts': qs })
