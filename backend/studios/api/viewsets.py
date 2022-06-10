from rest_framework import viewsets, mixins

from utils.pagination import StandardResultsSetPagination
from studios.api.serializers import StudioSerializer
from studios.models import Studio


class StudioViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Studio.objects.order_by("-id")

    def get_serializer_class(self):
        return StudioSerializer
