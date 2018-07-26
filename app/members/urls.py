from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('facebook-login/', views.facebook_login, name='facebook-login'),
]
