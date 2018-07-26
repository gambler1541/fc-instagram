from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def login_view(request):
    # 1. POST요청이 왔는데, 요청이 올바르면서 <- 코드에서 어느 위치인지 파악
    # 2.  GET paramter에 'next'값이 존재할 경우 <-- GET parameter는 request.GET으로 접근
    # 3.  해당 값(URL)으로 redirect <- redirect()함수는 URL문자열로도 이동 가능
    # 4.  next값이 존재하지 않으면 원래 이동하던 곳으로 그대로 redirect <- 문자열이 있는지 없는지는 if로 판단

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

            # session_id값을 django_sessions테이블에 저장, 데이터는 user와 연결됨
            # 이 함수 실행 후 돌려줄 HTTP Response에는 Set-Cookie헤더를 추가, 내용은 sessionid=<session값>
            login(request, user)
            print(request.GET)

            # GET parameter에 'next'값이 전달되면 해당 값으로 redirect
            next = request.GET.get('next')
            if next:
                return redirect(next)
            # next값이 전달되지 않았으면 post-list로 redirect
            return redirect('posts:post-list')

        # 인증에 실패한 경우 (username또는 password가 틀린 경우)
        else:
            # 다시 로그인 페이지로 redirect
            return redirect('members:login')
    # GET 요청일 경우
    else:
        # form이 있는 template을 보여준다
        return render(request, 'members/login.html')

