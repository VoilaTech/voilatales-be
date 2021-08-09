from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
import random

time_creation = datetime.now().timestamp()

def otp_gen():
    return random.randrange(99999, 999999)

class getRegistered(APIView):
    def post(self, request):
        time_creation = datetime.now().timestamp()
        phone = request.data.get("phone")
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
        phone_number.save()  # Save the data
        return Response({"OTP": phone_number.otp}, status=200)  # Just for demonstration


class getVerified(APIView):
    def post(self, request):
        # import pdb; pdb.set_trace() 
        try:
            phone_number = User.objects.get(phone_number=request.data.get("phone"))
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = phone_number.otp
        if datetime.now().timestamp() - time_creation < 50:
            if keygen == request.data["otp"]:  # Verifying the OTP
                phone_number.isVerified = True
                phone_number.otp=None
                phone_number.save()
                return Response("You are authorised", status=200)
            return Response("OTP is wrong", status=400)
        else:
            return Response("OTP is expired", status=400)
        


        