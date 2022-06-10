from rest_framework import viewsets, mixins

from utils.pagination import StandardResultsSetPagination
from news.api.serializers import NewSerializer
from news.models import New


class NewViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return New.objects.order_by("-id")

    def get_serializer_class(self):
        return NewSerializer
