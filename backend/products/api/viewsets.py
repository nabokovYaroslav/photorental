from datetime import datetime
from django.db.models import Prefetch, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from products.api.serializers import ProductSerializer, CharacteristicSerializer, ProductReservedQuantity
from utils.pagination import StandardResultsSetPagination
from products.models import Product, Value
from orders.models import ProductsToOrder


class CategoryProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category_id = self.kwargs.get("category_pk", None)
        queryset = Product.objects.filter(category_id=category_id)
        if self.action == "list":
            eav_filters = {}
            query_params = self.request.GET
            for key in query_params:
                fields = key.split("__")
                if fields[0] == "eav" and len(fields) > 2:
                    if fields[2] == "enum":
                        eav_key = "{key}__{lookup}".format(key=key, lookup="in")
                        value = query_params.getlist(key)
                        eav_filters[eav_key] = value
            for key, value in eav_filters.items():
                product_ids = Value.objects.filter(**{key: value}).values_list("product_id", flat=True).distinct()
                queryset = queryset.filter(id__in=product_ids)
            return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ProductSerializer

class ProductViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        if self.action in ("list", "retrieve", "products_reserved_quantity", "products_in_cart"):
            return Product.objects.all()
        elif self.action == "characteristics":
            return Value.objects.select_related("value_enum", "attribute__group").order_by("attribute__group__order")
        elif self.action == "new_products":
            return Product.objects.order_by("-id")
        elif self.action == "top_products":
            return Product.objects.annotate(count_product_in_orders=Coalesce(Sum("product_in_orders__count"), 0)).order_by("-count_product_in_orders")

    def get_serializer_class(self):
        if self.action in ("list", "retrieve", "new_products", "top_products", "products_in_cart"):
            return ProductSerializer
        elif self.action == "products_reserved_quantity":
            return ProductReservedQuantity
        elif self.action == "characteristics":
            return CharacteristicSerializer

    @action(detail=True, methods=("get",))
    def characteristics(self, request, pk=None):
        queryset = self.get_queryset().filter(product_id=pk)
        serializer = self.get_serializer(queryset, many=True)

        data = []
        for characteristic in serializer.data:
            attribute = characteristic["attribute"] 
            group = next((group for group in data if attribute["group_id"] == group["id"]), None)
            if group is None:
                data.append({"id": attribute["group_id"], "name": attribute["group_name"], "attributes": [{"id": attribute["id"], "name": attribute["name"], "value": characteristic["value"]}]})
            else:
                group["attributes"].append({"id": attribute["id"], "name": attribute["name"], "value": characteristic["value"]})
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("get",))
    def products_reserved_quantity(self, request):
        product_ids = request.GET.getlist("id")
        start_date = request.GET.get("start_date", None)
        try:
            if start_date is None:
                raise ValueError
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            return Response({"start_date": "Неверный формат"}, status=status.HTTP_400_BAD_REQUEST)

        end_date = request.GET.get("end_date", None)
        try:
            if end_date is None:
                raise ValueError
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%f%z")
        except ValueError:
            return Response({"end_date": "Неверный формат"}, status=status.HTTP_400_BAD_REQUEST)
            

        queryset = (
                    ProductsToOrder
                    .objects
                    .select_related("order")
                    .filter(order__start_date__gte=start_date, order__end_date__lte=end_date, product_id__in=product_ids)
                    .values("product_id")
                    .annotate(reserved_quantity=Coalesce(Sum("count"), 0))
        )
        second_queryset = self.get_queryset().filter(id__in=product_ids).values("id")
        for product in second_queryset:
            product["reserved_quantity"] = next((product_to_order["reserved_quantity"] for product_to_order in queryset if product_to_order["product_id"] == product["id"]), 0)
        serializer = self.get_serializer(second_queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=("get",))
    def new_products(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=("get",))
    def top_products(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=("get",))
    def products_in_cart(self, request):
        id = request.GET.getlist("id", [])
        queryset = self.get_queryset().filter(id__in=id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)