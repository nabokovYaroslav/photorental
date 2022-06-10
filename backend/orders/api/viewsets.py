from django.db import transaction
from rest_framework import viewsets, mixins

from orders.api.serializers import OrderCreateSerializer
from products.models import Product


class OrderViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):

    def get_serializer_class(self):
        return OrderCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        products = request.data.get("products", [])
        if not isinstance(products, list):
            products = []
        product_ids = [product.get("id", None) for product in products]
        Product.objects.filter(id__in=product_ids).select_for_update()
        return super().create(request, *args, **kwargs)