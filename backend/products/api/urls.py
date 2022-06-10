from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter

from products.api.viewsets import ProductViewSet


router = SimpleRouter()

router.register("", viewset=ProductViewSet, basename="products")

urlpatterns = [
    path("", include(router.urls))
]
