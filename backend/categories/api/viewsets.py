from rest_framework.decorators import action
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from categories.api.serializers import CategorySerializer, FilterSerializer
from categories.models import Category
from products.models import Attribute


class CategoryViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    def get_queryset(self):
        if self.action == "list":
            return Category.objects.all()
        return Attribute.objects.filter(datatype="enum")

    def get_serializer_class(self):
        if self.action == "list":
            return CategorySerializer
        return FilterSerializer

    @action(detail=True, methods=("get",))
    def filters(self, request, pk=None):
        queryset = self.get_queryset().filter(category_id=pk)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
