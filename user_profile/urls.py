from django.urls import path
from .views import getRegistered, getVerified, LogoutView

urlpatterns = [
    path("", getRegistered.as_view(), name="OTP Gen"),
    path("otp", getVerified.as_view(), name="OTP verify"),
    path("logout", LogoutView.as_view(), name="logout"),
]