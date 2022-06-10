from rest_framework import viewsets, mixins

from faq.api.serializers import FAQSerializer
from faq.models import FAQ


class FAQViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer