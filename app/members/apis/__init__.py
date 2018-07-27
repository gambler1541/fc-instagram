from django.contrib.auth import get_user_model
from rest_framework import generics

from members.userserializers import UserSerializer

User=get_user_model()

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer