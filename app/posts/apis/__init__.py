from django.contrib.auth import get_user_model
from rest_framework import generics



from ..serializers import PostSerializer
from ..models import Post

User = get_user_model()

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


