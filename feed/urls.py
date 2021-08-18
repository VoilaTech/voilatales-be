from django.urls import path
from .views import PostList,PostDelete

urlpatterns = [
    path("create", PostList.as_view(), name="post create"),
    path("delete/<uuid:pk>", PostDelete.as_view(), name="post delete")
]