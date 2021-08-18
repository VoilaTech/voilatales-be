from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

class PostCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user_id = self.request.user)

class PostDelete(generics.RetrieveDestroyAPIView):
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
    