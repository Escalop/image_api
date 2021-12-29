from garpixcms.urls import *  # noqa
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from api.views.views import RegisterUserView
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [] + [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('docs/', include_docs_urls(title='PhotoAlbum')),
    path('schema', get_schema_view(
        title="PhotoAlbum",
        description="API for the PhotoAlbum",
        version="1.0.0",),
        name='openapi-schema'
    )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
