from django.urls import path
from .views import getRegistered, getVerified, LogoutView, UserRelationshipView, UserList, UserRetrive

urlpatterns = [
    path("auth", getRegistered.as_view(), name="OTP Gen"),
    path("verify-otp", getVerified.as_view(), name="OTP verify"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("follow", UserRelationshipView.as_view(), name="follow"),
    path("follow/<str:username>/", UserRelationshipView.as_view(), name="follow data"),
    path("list", UserList.as_view(), name="user list"),
    path("<str:username>", UserRetrive.as_view(), name="user data"),
]