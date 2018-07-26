
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect


User = get_user_model()

__all__ = (
    'facebook_login',
)


def facebook_login(request):
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    print(user)
    print(type(user))
    if user is not None:
        login(request, user)
        return redirect('index')
    return redirect('members:login')
