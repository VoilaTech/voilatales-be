from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django_comments_xtd.views import XtdCommentListView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Tales API",
      default_version='v1',
      description="Api for Voila Tales app",
      contact=openapi.Contact(email="voilatect.rv@gmail.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user_profile.urls')),
    path('tales/', include('feed.urls')),
    path('comments/', include('django_comments_xtd.urls')),
    path('comments/', XtdCommentListView.as_view(content_types=["feed.post",],paginate_by=10, page_range=5),
            name='comments-xtd-list'),
    path('docs.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
