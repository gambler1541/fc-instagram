from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

# User클래스 자체를 가져올때는 get_user_model()
# ForeignKey에 User모델을 지정할때는 settings.AUTH_USER_MODEL
User = get_user_model()


def login_view(request):
    # 1. member.urls <- 'members/'로 include되도록 config.urls모듈에 추가
    # 2. path구현 (URL: '/members/login/')
    # 3. path와 이 view연결
    # 4. 일단 잘 나오는지 확인
    # 5. 잘 나오면 form을 작성 (username, password를 받는 input2개)
    #   templates/members/login.html에 작성

    # 6. form작성후에는 POST방식 요청을 보내서 이 뷰에서 request.POST에 요청이 잘 왔는지 확인
    # 7. 일단은 받은 username, password값을 HttpResponse에 보여주도록 한다.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(request.user.is_authenticated)
        # 받은 username과 password에 해당하는 User가 있는지 인증
        user = authenticate(request, username=username, password=password)

        # 인증에 성공한 경우
        if user is not None:
            # 세션값을 만들어 DB에 저장하고, HTTP response의 Cookie에 해당값을 담아보내도록 하는
            # login()함수를 실행한다
            login(request, user)
            print(request.user.is_authenticated)
            # 이후 post-list로 redirect
            return redirect('posts:post-list')
        # 인증에 실패한 경우 (username또는 password가 틀린 경우)
        else:
            # 다시 로그인 페이지로 redirect
            return redirect('members:login')
    # GET 요청일 경우
    else:
        # form이 있는 template을 보여준다
        return render(request, 'members/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')


from .forms import SignupForm


def signup(request):
    # form.is_valid()를 통과하지 못한 경우,
    #  유효성 검증을 통과하지 못한 내용은 form.<field>.errors에 정의됨 -> form을 순회하면 form.<field>를 하나씩 순회
    #  (통과하지 못한 경우의 'form'변수를 디버깅을 이용해 확인해본다)

    # 1. form.is_valid()를 통과하지 못했을 경우, 해당 내용을 template에 출력하도록 구현
    # 2. SignupForm의 clean()메서드를 재정의하고, password와 password2를 비교해서 유효성을 검증하도록 구현
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # form에 들어있는 데이터가 유효한지 검사
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            login(request, user)
            return redirect('index')
        else:
            result = '\n'.join(['{}: {}'.format(key, value) for key, value in form.errors.items()])
            return HttpResponse(result)
    else:
        form = SignupForm()
        context = {
            'form': form,
        }
        return render(request, 'members/signup.html', context)


def signup_bak(request):
    context = {
        'errors': [],
    }
    if request.method == 'POST':
        # username, email, password, password2에 대해서
        # 입력되지 않은 필드에 대한 오류를 추가
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # 반드시 내용이 채워져야 하는 form의 필드 (위 변수명)
        # hint: required_fields를 dict로
        # required_fields = ['username', 'email', 'password', 'password2']
        required_fields = {
            'username': {
                'verbose_name': '아이디',
            },
            'email': {
                'verbose_name': '이메일',
            },
            'password': {
                'verbose_name': '비밀번호',
            },
            'password2': {
                'verbose_name': '비밀번호 확인',
            },
        }
        for field_name in required_fields.keys():
            if not locals()[field_name]:
                context['errors'].append('{}을(를) 채워주세요'.format(
                    required_fields[field_name]['verbose_name'],
                ))

        # # for문으로 작동하도록 수정
        # if not username:
        #     context['errors'].append('username을 채워주세요')
        # if not email:
        #     context['errors'].append('email을 채워주세요')
        # if not password:
        #     context['errors'].append('password를 채워주세요')
        # if not password2:
        #     context['errors'].append('password2를 채워주세요')

        # 입력데이터 채워넣기
        context['username'] = username
        context['email'] = email

        # form에서 전송된 데이터들이 올바른지 검사
        if User.objects.filter(username=username).exists():
            context['errors'].append('유저가 이미 존재함')
        if password != password2:
            context['errors'].append('패스워드가 일치하지 않음')

        # errors가 없으면 유저 생성 루틴 실행
        if not context['errors']:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
            )
            login(request, user)
            return redirect('index')
    return render(request, 'members/signup.html', context)
