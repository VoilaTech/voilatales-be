from django.urls import path
from .views import getRegistered, getVerified

urlpatterns = [
    path("", getRegistered.as_view(), name="OTP Gen"),
    path("otp", getVerified.as_view(), name="OTP verify"),
]