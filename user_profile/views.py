from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
import base64



class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


EXPIRY_TIME = 300 # seconds

class getRegistered(APIView):

    # Get to Create a call for OTP
	# @staticmethod
	def post(self, request):
		phone = request.data.get("phone")
		display_name=request.data.get("display_name")
		username= request.data.get("username")
		display_image=request.data.get("display_image")
		print()
		print(type(phone))
		try:
			phone_number = User.objects.get(phone_number=phone)  # if Mobile already exists the take this else create New One
		except ObjectDoesNotExist:
		    User.objects.create(
		        phone_number=phone,
		        display_name=display_name,
		        username= username,
		        display_image=display_image,
		        isVerified = False
		    )
		    phone_number = User.objects.get(phone_number=phone)  # user Newly created Model
		phone_number.save()  # Save the data
		keygen = generateKey()
		key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
		OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model for OTP is created
		print(OTP.now())
		# Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
		return Response({"OTP": OTP.now()}, status=200)  # Just for demonstration


class getVerified(APIView):
    # This Method verifies the OTP
    # @staticmethod
    def post(self, request):
        try:
            phone_number = User.objects.get(phone_number=request.data.get("phone"))
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(request.data.get("phone")).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model 
        if OTP.verify(request.data["otp"]):  # Verifying the OTP
            phone_number.isVerified = True
            phone_number.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong/expired", status=400)