# config.urls에서
#   path('posts/', include('posts.urls'))

# posts.urls에서 지정
# post_list(request)
#  -> '/posts/'
# post_detail(request, pk) <- view parameter 및 path패턴명에 'pk'사용
#  -> /posts/3/

# 구현하세요
# base.html기준으로
#   TEMPLATE설정 쓸 것 (templates폴더를 DIRS에 추가)
#                       -> 경로이름은 TEMPLATES_DIR로 settings.py의 윗부분에 추가

# post_list는   'posts/post_list.html'
# post_detail은 'posts/post_detail.html' 사용

# 1. view와 url의 연결 구현
# 2. view에서 template을 렌더링하는 기능 추가
# 3. template에서 QuerySet또는 object를 사용해서 객체 출력
# 4. template에 extend사용
from django.shortcuts import render

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)
