from django.urls import path

from .. import apis

urlpatterns = [
    path('', apis.PostList.as_view()),
]