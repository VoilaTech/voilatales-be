from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from user_profile.models import User

class PostList(generics.ListAPIView):
    '''
        ## Tale List view
        ---
        ### It returns all the tales exist
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]
    # def get_queryset(self):
    #     user = User.objects.get(username=self.kwargs['username'])
    #     return Post.objects.filter(user=user)

class PostCreate(generics.CreateAPIView):
    '''
        ## Tale create view
        ---
        ### It takes tale description, tale cover image, and tale
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class PostDelete(generics.DestroyAPIView):
    '''
        ## Tale delete view
    '''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,]
    def destroy(self, *args, **kwargs):
        obj = self.get_object()
        if obj.user.id == self.request.user.id:
            self.perform_destroy(obj)
            return Response(data={'message': "Successfully deleted"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={'message': "Your not authorized to delete"},status=status.HTTP_401_UNAUTHORIZED)
    