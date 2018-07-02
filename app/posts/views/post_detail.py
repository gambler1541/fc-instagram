from django.shortcuts import render

from ..models import Post

__all__ = (
    'post_detail',
)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)
