from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter

from studios.api.viewsets import StudioViewSet


router = SimpleRouter()

router.register("", viewset=StudioViewSet, basename="studios")

urlpatterns = [
    path("", include(router.urls)),
]
