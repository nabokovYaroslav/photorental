import os

from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from categories.models import Category
from products.managers import ValueManager

class Product(models.Model):
    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/recipes/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    name = models.CharField(max_length=255, verbose_name="Название товара")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория товара")
    image = models.ImageField(upload_to=upload_to, max_length=255, verbose_name="Фотография")
    description = models.TextField(verbose_name="Описание")
    price = models.PositiveIntegerField(verbose_name="Цена в сутки")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def available_quantity(self, start_date, end_date):
        reserved_quantity = (
            self.product_in_orders.select_related("order")
            .filter(order__start_date__gte=start_date, order__end_date__lte=end_date)
            .aggregate(reserved_quantity=Coalesce(Sum("count"), 0))
        )
        return self.quantity - reserved_quantity["reserved_quantity"]

    def __str__(self):
        return "Категория: {} | Товар: {}".format(self.category.name, self.name)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class EnumGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название группы выбора")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа выбора"
        verbose_name_plural = "Группы выбора"

class AttributeGroup(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    order = models.PositiveSmallIntegerField(verbose_name="Порядок отображения", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа атрибута"
        verbose_name_plural = "Группы атрибутов"

class Attribute(models.Model):
    DATATYPE_CHOICES = (
        ("text", ("Текст")),
        ("varchar", ("Короткий текст")),
        ("enum", ("Выборочный")),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    datatype = models.CharField(choices=DATATYPE_CHOICES, max_length=50, verbose_name="Тип данных")
    group = models.ForeignKey(AttributeGroup, on_delete=models.CASCADE, verbose_name="Группа")
    name = models.CharField(max_length=100, verbose_name="Название", help_text="Дружественное для пользователя")
    slug = models.CharField(max_length=100, unique=True, verbose_name="Уникальное название атрибута")

    enum_group = models.ForeignKey(
        EnumGroup, 
        on_delete=models.PROTECT, 
        verbose_name="Группа выбора",
        blank=True,
        null=True, 
    )

    def save(self, *args, **kwargs):
        self.enum_group = None if self.datatype != "enum" else self.enum_group
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Название атрибута: {} | Тип данных: {}".format(self.name, self.datatype)

    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'

class EnumValue(models.Model):
    enum_group = models.ForeignKey(EnumGroup, on_delete=models.CASCADE, related_name="enum_group_values", verbose_name="Группа выбора")
    value = models.CharField(max_length=255, verbose_name="Значение")

    def __str__(self):
        return "Группа выбора: {} | Значение: {}".format(self.enum_group.name, self.value)

    class Meta:
        verbose_name = "Значение группы выбора"
        verbose_name_plural = "Значения группы выбора"

class Value(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, verbose_name="Атрибут")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")

    value_varchar = models.CharField(max_length=255, blank=True, verbose_name="Значение")
    value_text = models.TextField(blank=True, verbose_name="Значение")
    value_enum = models.ForeignKey(EnumValue, related_name="enum_values", on_delete=models.PROTECT, null=True, blank=True, verbose_name="Значение")

    def _get_value(self):
        attribute = getattr(self, 'value_{0}'.format(self.attribute.datatype))
        if self.attribute.datatype == "enum":
            return attribute.value
        return attribute

    def _set_value(self, value):
        setattr(self, 'value_{0}'.format(self.attribute.datatype), value)

    value = property(_get_value, _set_value)

    objects = ValueManager()

    def save(self, *args, **kwargs):
        self.value_varchar = "" if self.attribute.datatype != "varchar" else self.value_varchar
        self.value_text = "" if self.attribute.datatype != "text" else self.value_text
        self.value_enum = None if self.attribute.datatype != "enum" else self.value_enum
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Товар: {} | Название атрибута: {} | Значение атрибута: {}".format(self.product.name, self.attribute.name, self.value)

    class Meta:
        verbose_name = "Значение атрибута"
        verbose_name_plural = "Значения атрибутов"
        unique_together = ["attribute", "product"]