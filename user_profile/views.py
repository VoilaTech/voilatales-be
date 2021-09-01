from datetime import datetime
from django.core import exceptions
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, UserRelationship
import random
import requests
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import uuid
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
time_creation = datetime.now().timestamp()
def otp_gen():
    return random.randrange(99999, 999999)

class getRegistered(APIView):
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
            querystring = {"authorization":"b7YBvi3RELWtZau6nCSpsH9AogKhJdrcNTeFwqm0yQX14zlVOUeKqkxBZd8JDXFC1s3ENQvj9HY2t0mi","variables_values":str(phone_number.otp),"route":"otp","numbers": number}
            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            return Response({"OTP": phone_number.otp}, status=200)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class getVerified(APIView):
    def post(self, request):
        try:
            phone_number = User.objects.get(phone_number=request.data.get("phone_number"))
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = phone_number.otp
        if datetime.now().timestamp() - time_creation < 500:
            if keygen == request.data["otp"]:  # Verifying the OTP
                phone_number.isVerified = True
                token  = Token.objects.create(user=phone_number)
                phone_number.otp=None
                phone_number.save()
                return Response({"Token": str(token)}, status=200)
            return Response("OTP is wrong", status=400)
        else:
            return Response("OTP is expired", status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def delete(self,request, *args, **kwargs):
        self.request.user.auth_token.delete()
        data = {
            "message": "You have successfully logged out.",
        }
        return Response(data, status=status.HTTP_200_OK)



class UserRelationshipView(APIView):
    def post(self, request):
        user = User.objects.get(id=self.request.user.id)
        followinguser = User.objects.get(id=uuid.UUID(self.request.data.get('following_id')))
        userfollow = UserRelationship.objects.filter(user_id=user, following_user_id=followinguser)
        if userfollow:
            userfollow.delete()
            return Response("Successfully Unfollowed", status=status.HTTP_200_OK)
        else:
            UserRelationship.objects.create(user_id=user, following_user_id=followinguser)
            return Response("Successfully followed", status=status.HTTP_200_OK)
    def get(self, request,id):
        user = User.objects.get(id=uuid.UUID(id))
        following = UserRelationship.objects.filter(user_id=user).values_list('following_user_id')
        follower = UserRelationship.objects.filter(following_user_id=user).values_list('user_id')
        following_users = []
        follower_users = []
        for i in following:
            temp_user=User.objects.get(id=i[0])
            temp = {}
            temp["username"] = temp_user.username
            temp["display_name"] = temp_user.display_name
            temp["id"] = temp_user.id
            following_users.append(temp)
        for i in follower:
            temp_user=User.objects.get(id=i[0])
            temp = {}
            temp["username"] = temp_user.username
            temp["display_name"] = temp_user.display_name
            temp["id"] = temp_user.id
            follower_users.append(temp)
        return JsonResponse({"status": 200, "data": {"following" : following_users, "follower": follower_users, "following_count": len(following_users), "follower_count": len(follower_users)}})

# ef7c51fb0ac7537d2ad4cc1caad8c775b61f51ae
# 1c2813ae403c6da0f6f79b3fde4c96d6d72c9919
# a595a3b8fa49ec0064feb923d33a7a5457559132