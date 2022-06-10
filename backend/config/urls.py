from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/categories/", include("categories.api.urls")),
    path("api/v1/news/", include("news.api.urls")),
    path("api/v1/studios/", include("studios.api.urls")),
    path("api/v1/products/", include("products.api.urls")),
    path("api/v1/orders/", include("orders.api.urls")),
    path("api/v1/faq/", include("faq.api.urls")),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else urlpatterns