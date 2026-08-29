from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.catalog.urls")),
    path("cart/", include("apps.cart.urls")),
    path("", include("apps.orders.urls")),
    path("contact/", include("apps.contact.urls")),
    path("newsletter/", include("apps.newsletter.urls")),
]
# Coolify persists user uploads at MEDIA_ROOT. WhiteNoise serves static assets;
# this lightweight Django route keeps uploaded media available from the single app container.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
