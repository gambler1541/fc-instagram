from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import PostSerializer
from ..models import Post


class PostList(APIView):
    def get(self, request, format=None):
        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

