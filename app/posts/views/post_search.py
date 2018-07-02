from django.shortcuts import render

from ..models import Post

__all__ = (
    'search_post_list',
)


def search_post_list(request, tag):
    posts = Post.objects.filter(tags__name=tag).distinct()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/search_post_list.html', context)
