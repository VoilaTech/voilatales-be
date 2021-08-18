from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        # import pdb; pdb.set_trace()
        serializer.save(user_id = self.request.user)

class PostList(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]
    