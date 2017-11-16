from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from . import apis, views

urlpatterns = [
    url(f'^', include(views)),
    url(f'^api/', include(apis, namespace='api')),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
