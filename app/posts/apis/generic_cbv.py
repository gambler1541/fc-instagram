from rest_framework import generics, permissions

from posts.serializers import PostSerializer
from ..models import Post


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSerializer
