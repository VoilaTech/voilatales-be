from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user_profile.models import User

class PostList(generics.ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]
    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        return Post.objects.filter(user_id=user)

class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user_id = self.request.user)

class PostDelete(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]
    def destroy(self, *args, **kwargs):
        obj = self.get_object()
        if obj.user_id.id == self.request.user.id:
            self.perform_destroy(obj)
            return Response(data={'message': "Successfully deleted"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={'message': "Your not authorized to delete"},status=status.HTTP_401_UNAUTHORIZED)
    