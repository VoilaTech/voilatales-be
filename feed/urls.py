from django.urls import path
from .views import PostList,PostDelete, PostCreate

urlpatterns = [
    path("<str:username>", PostList.as_view(), name="tale list"),
    path("create", PostCreate.as_view(), name="create tale"),
    path("delete/<uuid:pk>", PostDelete.as_view(), name="delete tale")
]