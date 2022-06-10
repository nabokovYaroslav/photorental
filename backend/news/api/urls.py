from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter

from news.api.viewsets import NewViewSet


router = SimpleRouter()

router.register("", viewset=NewViewSet, basename="news")

urlpatterns = [
    path("", include(router.urls))
]
