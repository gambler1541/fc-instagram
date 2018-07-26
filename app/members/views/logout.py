from django.contrib.auth import logout
from django.shortcuts import redirect

__all__ = (
    'logout_view',
)
def logout_view(request):
    logout(request)
    return redirect('index')
