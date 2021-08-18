from django.urls import path
from .views import PostList,PostDelete, PostCreate

urlpatterns = [
    path("", PostList.as_view(), name="post list"),
    path("create", PostCreate.as_view(), name="post create"),
    path("delete/<uuid:pk>", PostDelete.as_view(), name="post delete")
]