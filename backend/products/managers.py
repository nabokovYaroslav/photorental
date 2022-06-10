from django.db import models

from products.querysets import EAVQuerySet


class ValueManager(models.Manager):
    
    _queryset_class = EAVQuerySet