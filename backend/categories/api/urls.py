from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from django.urls import path, include

from categories.api.viewsets import CategoryViewSet
from products.api.viewsets import CategoryProductViewSet


router = SimpleRouter()

router.register("", viewset=CategoryViewSet, basename="categories")

category_router = NestedSimpleRouter(router, "", lookup="category")
category_router.register("products", viewset=CategoryProductViewSet, basename="products of category")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(category_router.urls))
]
