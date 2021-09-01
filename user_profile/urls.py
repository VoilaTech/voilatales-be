from django.urls import path
from .views import getRegistered, getVerified, LogoutView, UserRelationshipView

urlpatterns = [
    path("", getRegistered.as_view(), name="OTP Gen"),
    path("otp", getVerified.as_view(), name="OTP verify"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("follow", UserRelationshipView.as_view(), name="follow"),
    path("follow/<str:id>/", UserRelationshipView.as_view(), name="follow data"),
]