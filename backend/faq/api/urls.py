from rest_framework_nested.routers import SimpleRouter
from django.urls import path, include

from faq.api.viewsets import FAQViewSet


router = SimpleRouter()

router.register("", viewset=FAQViewSet, basename="FAQ's")

urlpatterns = [
    path("", include(router.urls))
]
