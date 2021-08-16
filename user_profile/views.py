from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
import random
import requests
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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
        


        