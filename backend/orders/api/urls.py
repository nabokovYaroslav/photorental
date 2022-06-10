from rest_framework_nested.routers import SimpleRouter
from django.urls import path, include

from orders.api.viewsets import OrderViewSet


router = SimpleRouter()

router.register("", viewset=OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
