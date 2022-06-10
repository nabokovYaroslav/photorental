from rest_framework import serializers

from categories.models import Category
from products.models import EnumGroup, EnumValue, Attribute


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class EnumValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = EnumValue
        fields = ("id", "value")

class EnumGroupSerializer(serializers.ModelSerializer):
    choices = EnumValueSerializer(many=True, source="enum_group_values")

    class Meta:
        model = EnumGroup
        fields = ("name", "choices")

class FilterSerializer(serializers.ModelSerializer):
    enum_group = EnumGroupSerializer()

    class Meta:
        model = Attribute
        fields = ("id", "datatype", "name", "slug", "enum_group")