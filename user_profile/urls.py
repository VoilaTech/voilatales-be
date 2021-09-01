from django.urls import path
from .views import getRegistered, getVerified, LogoutView, UserFollowingViewSet

urlpatterns = [
    path("", getRegistered.as_view(), name="OTP Gen"),
    path("otp", getVerified.as_view(), name="OTP verify"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("follow", UserFollowingViewSet.as_view({'get': 'list','post': 'create'}), name="follow"),
]