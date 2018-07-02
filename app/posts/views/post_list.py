from django.shortcuts import render

from ..models import Post

__all__ = (
    'post_list',
)


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)
