from django.urls import path, include

urlpatterns = [
    path('', include('config.urls.views')),
    path('api/', include('config.urls.apis'))
]