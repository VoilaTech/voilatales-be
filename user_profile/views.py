from datetime import datetime
from feed.models import Post
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, UserRelationship
import random
import requests
from .serializers import UserSerializer, UserVerifySerializer, UserRelationshipSerializer,UserUpdateSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import uuid
from django.http import JsonResponse
from rest_framework import generics
from decouple import config
from rest_framework.generics import GenericAPIView 

time_creation = datetime.now().timestamp()
def otp_gen():
    return random.randrange(99999, 999999)

class getRegistered(GenericAPIView):
    '''
        ## Signin or Signup view
        ---
        ### For Signin - it takes phone number
        ### For Signup - it takes phone number, display name, username, display image(optional)
    '''
    serializer_class = UserSerializer
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            time_creation = datetime.now().timestamp()
            phone = request.data.get("phone_number")
            display_name=request.data.get("display_name")
            username= request.data.get("username")
            display_image=request.data.get("display_image")
            try:
                phone_number = User.objects.get(phone_number=phone)
                phone_number.otp = otp_gen()
            except ObjectDoesNotExist:
                User.objects.create(
                phone_number=phone,
                display_name=display_name,
                username= username,
                display_image=display_image,
                isVerified = False,
                otp = otp_gen()
                )
                phone_number = User.objects.get(phone_number=phone)  # user Newly created Model
            phone_number.save()
            url = "https://www.fast2sms.com/dev/bulkV2"
            number = (str(phone_number.phone_number))[3:]
            querystring = {"authorization":config('AUTHORIZATION'),"variables_values":str(phone_number.otp),"route":"otp","numbers": number}
            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            return Response({"OTP": phone_number.otp}, status=200)  
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getVerified(GenericAPIView):
    '''
        ## Verify user view
        ---
        ### It takes phone number and otp(which is sent through sms)
    '''
    serializer_class = UserVerifySerializer
    def post(self, request):
        try:
            user = User.objects.get(phone_number=request.data.get("phone_number"))
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = user.otp
        if datetime.now().timestamp() - time_creation < int(config('TIME')):
            if keygen == request.data["otp"]:  # Verifying the OTP
                user.isVerified = True
                try:
                    token = Token.objects.get(user=user)
                except:
                    token  = Token.objects.create(user=user)
                user.otp=None
                user.save()
                data = {
                    "Token": str(token),
                    "username": user.username,
                    "display_name": user.display_name,
                    "display_image": user.get_profile_pic_url(),
                    "id": user.id
                }
                return Response(data, status=200)
            return Response("OTP is wrong", status=400)
        else:
            return Response("OTP is expired", status=400)

class LogoutView(APIView):
    '''
        ## Logout view
    '''
    permission_classes = [IsAuthenticated,]
    
    def delete(self,request, *args, **kwargs):
        self.request.user.auth_token.delete()
        data = {
            "message": "You have successfully logged out.",
        }
        return Response(data, status=status.HTTP_200_OK)



class UserPostRelationshipView(GenericAPIView):
    '''
        ## Follow/UnFollow view
        ---
        ### For Follow - it takes 2 user id, where user1 follows user2
        ### For UnFollow - it takes 2 user id, where user1 unfollows user2
    '''
    serializer_class = UserRelationshipSerializer
    def post(self, request):
        user = User.objects.get(id=self.request.user.id)
        followinguser = User.objects.get(id=uuid.UUID(self.request.data.get('following_id')))
        userfollow = UserRelationship.objects.filter(user=user, following_user=followinguser)
        if userfollow:
            userfollow.delete()
            return Response("Successfully Unfollowed", status=status.HTTP_200_OK)
        else:
            UserRelationship.objects.create(user=user, following_user=followinguser)
            return Response("Successfully followed", status=status.HTTP_200_OK)
class UserDataView(APIView):
    '''
        ## User Data view
        ---
        ### It takes a username
        ### Returns
        ` data = {
            user: {},
            posts: [], 
            followings: [],
            followers: [], 
            followings count: int,
            followers count: int
        }`
    '''
    def get(self, request,username):
        user = User.objects.get(username=username)
        posts = Post.objects.filter(user=user).values()
        following = UserRelationship.objects.filter(user=user).values_list('following_user', flat=True)
        follower = UserRelationship.objects.filter(following_user=user).values_list('user', flat=True)
        user_data={
            "username" : user.username,
            "display_name" : user.display_name,
            "id" : user.id,
            "display_image" : user.get_profile_pic_url(),
        }
        following_data = []
        follower_data = []
        for i in posts:
            i["cover_image"] = config('BASEURL') + "/media/" + i["cover_image"]
            i["audio_field"] = config('BASEURL') + "/media/" + i["audio_field"]
        for i in following:
            temp_user=User.objects.get(id=i)
            temp = {}
            temp["username"] = temp_user.username
            temp["display_name"] = temp_user.display_name
            temp["id"] = temp_user.id
            temp["display_image"] = temp_user.get_profile_pic_url(),
            following_data.append(temp)
        for i in follower:
            temp_user=User.objects.get(id=i)
            temp = {}
            temp["username"] = temp_user.username
            temp["display_name"] = temp_user.display_name
            temp["id"] = temp_user.id
            temp["display_image"] = temp_user.get_profile_pic_url(),
            follower_data.append(temp)

        return JsonResponse({"status": 200, "data": {"user": user_data, 'posts': list(posts), "following" : following_data, "follower": follower_data, "following_count": len(following_data), "follower_count": len(follower_data)}})


class UserList(generics.ListAPIView):
    '''
        ## User List view
        ---
        ### It returns all the existing users
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserUpdate(generics.UpdateAPIView):
    '''
        ## User Update view
        ---
        ### It takes username, display name, display image
    '''
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated,]

    def update(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)