from functools import wraps

from django.db import models


def expand_eav_filter(key, value):
    """
    Accepts key, value.
    Recurisively replaces any eav filter with a subquery.
    For example::
        key = 'eav__height__int'
        value = 5
    Would return::
        key = "attribute__slug"
        value = "height"
        key = "value_int"
        value = 5
    For example::
        key = 'eav__height__int__in'
        value = [5,9]
    Would return::
        key = "attribute__slug"
        value = "height"
        key = "value_int__in"
        value = [5,9]
    """
    
    fields = key.split('__')

    if len(fields) > 2 and fields[0] == "eav":
        slug = fields[1]
        datatype = fields[2]

        value_key = ''
        if datatype == "enum":
            lookup = '__value__{}'.format(fields[3]) if len(fields) > 3 else '__value'
            value_key = 'value_{}{}'.format(datatype, lookup)
        else:
            lookup = '__{}'.format(fields[3]) if len(fields) > 3 else ''
            value_key = 'value_{}{}'.format(datatype, lookup)
        kwargs = {value_key: value, 'attribute__slug': slug}

        return kwargs

    # Not an eav field, so keep as is
    return {key: value}

def eav_filter(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        nkwargs = {}

        for key, value in kwargs.items():
            
            nkwarg = expand_eav_filter(key, value)
            
            for nkey, nvalue in nkwarg.items():
                nkwargs[nkey] = nvalue

        return func(self, *args, **nkwargs)

    return wrapper

class EAVQuerySet(models.QuerySet):
    
    @eav_filter
    def filter(self, *args, **kwargs):
        return super().filter(*args, **kwargs)