from rest_framework import serializers

from products.models import Product, Attribute, EnumGroup, EnumValue, Value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"

class AttributeSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(read_only=True, source="group.name")
    group_id = serializers.IntegerField(read_only=True, source="group.id")

    class Meta:
        model = Attribute
        fields = ("id", "name", "group_name", "group_id",)

class CharacteristicSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = Value
        fields = ("attribute", "value",)

class ProductReservedQuantity(serializers.ModelSerializer):
    reserved_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ("id", "reserved_quantity",)
