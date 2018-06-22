from django.urls import path

from . import views

urlpatterns = [
    # config.urls
    #  path('posts/', include(이 urlpatterns))
    path('', views.post_list),
    path('<int:pk>/', views.post_detail),
]
