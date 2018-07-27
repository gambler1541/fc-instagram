from django.urls import path, include


urlpatterns = path('', include([
    path('posts/', include('posts.urls.apis')),
    path('users/', include('members.urls.apis')),
])),
