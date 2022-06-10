from django.db import transaction
from django.db.models import Sum, F
from django.core.exceptions import ValidationError
from rest_framework import serializers

from orders.models import Order, ProductsToOrder
from orders.validators import validate_start_date, validate_phone
from products.models import Product


class ProductsToOrderCreateSerializer(serializers.ModelSerializer):

    def validate_product(self, value):
        if value.quantity == 0:
            raise serializers.ValidationError("Данный товар не доступен для заказа")
        return value

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество товара не может быть меньше 1")
        return value

    class Meta:
        model = ProductsToOrder
        fields = "__all__"
        extra_kwargs = {"order": {"read_only": True}}

class OrderCreateSerializer(serializers.ModelSerializer):
    products_in_order = ProductsToOrderCreateSerializer(many=True, required=True)

    def validate_products_in_order(self, value):
        if value is None or len(value) == 0:
            raise serializers.ValidationError("Заказ должен иметь хотя бы один товар")
        return value

    def validate_start_date(self, value):
        try:
            validate_start_date(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.message)
        return value

    def validate_phone(self, value):
        try:
            validate_phone(value)
        except ValidationError as exc:
            raise serializers.ValidationError(exc.message)
        return value

    def validate(self, attrs):
        errors = {}
        try:
            if (attrs["end_date"].date() - attrs["start_date"].date()).days < 1:
                raise serializers.ValidationError(("end_date", ["Минимальный срок бронирования, должен быть не меньше 1 дня."]))
        except serializers.ValidationError as exc:
            if exc.detail[0] in errors:
                errors[exc.detail[0]].extend(exc.detail[1])
            else:
                errors[exc.detail[0]] = exc.detail[1]
        errors["products_in_order"] = []
        start_date = attrs["start_date"]
        end_date = attrs["end_date"]
        products_has_error = False
        for product_to_order in attrs["products_in_order"]:
            try:
                available_quantity = product_to_order["product"].available_quantity(start_date, end_date)
                if product_to_order["count"] > available_quantity:
                    raise serializers.ValidationError(("count", available_quantity))
                errors["products_in_order"].append({})
            except serializers.ValidationError as exc:
                products_has_error = True
                errors["products_in_order"].append({exc.detail[0]: exc.detail[1]})
        if not products_has_error:
            errors.pop("products_in_order")
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs

    def create(self, validated_data):
        products_data = validated_data.pop('products_in_order', [])

        if products_data is None:
            products_data = []

        with transaction.atomic():
            order = Order.objects.create(**validated_data, price=0)

            products_data = [{"order_id": order.id, **product} for product in products_data]
            products_objects = [ProductsToOrder(**product) for product in products_data]

            if products_objects:
                ProductsToOrder.objects.bulk_create(products_objects)
            
            total_price = (
                        ProductsToOrder
                        .objects
                        .filter(order_id=order.id)
                        .select_related("product")
                        .annotate(price=F("count") * F("product__price") * order.reserved_days)
                        .aggregate(total_price=Sum("price"))
                        )
            order.price = total_price["total_price"]
            order.save()
        return order

    class Meta:
        model = Order
        exclude = ("status", "products")
        extra_kwargs = {"price": {"read_only": True}}