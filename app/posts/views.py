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
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import PostForm
from .models import Post


# '/'에 접근했을 때 post_list URL로 이동 (root url접근시 자동으로)
#  redirect또는 HttpResponseRedirect사용
# 1. '/'에 접근했을때의 URL지정
# 2. '/'에 접근했을때의 view구현 (def index)
# 3. index view는 post_list로 redirect시켜주는 기능을 함

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


@require_POST
@login_required
def post_delete(request, pk):
    # if request.method != 'POST':
    #     return HttpResponseNotAllowed()
    # if not request.user.is_authenticated:
    #     return redirect('members:login')
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        raise PermissionDenied('지울 권한이 없습니다')
    post.delete()
    return redirect('posts:post-list')


def post_create(request):
    # PostModelForm을 사용
    #  form = PostModelForm(request.POST, request.FILES)
    #  post = form.save(commit=False)
    #  post.author = request.user
    #  post.save()
    pass


@login_required
def post_create_with_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(author=request.user)
            return redirect('posts:post-detail', pk=post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


def post_create_without_form(request):
    if request.method == 'POST':
        post = Post(
            author=request.user,
            photo=request.FILES['photo'],
            content=request.POST['content'],
        )
        post.save()
        return redirect('posts:post-detail', pk=post.pk)
    return render(request, 'posts/post_create.html')
