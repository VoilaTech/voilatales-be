from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django_comments_xtd.views import XtdCommentListView
# from rest_framework.documentation import include_docs_urls
from django_comments_xtd.views import XtdCommentListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_profile.urls')),
    path('post/', include('feed.urls')),
    path('comments/', include('django_comments_xtd.urls')),
    path('comments/', XtdCommentListView.as_view(content_types=["feed.post",],paginate_by=10, page_range=5),
            name='comments-xtd-list'),
    # path('', include_docs_urls(title='User Api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
