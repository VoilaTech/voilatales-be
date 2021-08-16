from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_profile.urls')),
    path('post/', include('feed.urls')),
    # path('', include_docs_urls(title='User Api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
