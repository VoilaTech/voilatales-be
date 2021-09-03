from django.urls import path
from .views import getRegistered, getVerified, LogoutView, UserPostRelationshipView, UserDataView, UserList, UserUpdate

urlpatterns = [
    path("auth", getRegistered.as_view(), name="OTP Gen"),
    path("verify-otp", getVerified.as_view(), name="OTP verify"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("follow", UserPostRelationshipView.as_view(), name="follow"),
    path("<str:username>", UserDataView.as_view(), name="follow data"),
    path("list", UserList.as_view(), name="user list"),
    path("update/", UserUpdate.as_view(), name="user update"),
]