from django.db import models
from django.core.exceptions import ValidationError

from products.models import Product
from orders.validators import validate_phone, validate_start_date


class Order(models.Model):
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    start_date = models.DateTimeField(verbose_name="Дата начала срока эксплуатации", validators=[validate_start_date])
    phone = models.CharField(max_length=13, verbose_name="Телефон", validators=[validate_phone])
    end_date = models.DateTimeField(verbose_name="Дата окончания срока эксплуатации")
    products = models.ManyToManyField(Product, through="ProductsToOrder", verbose_name="Товары")
    # should caclulated in creating order
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма заказа")

    STATUS_CHOICES = [
        ("new", "Новый заказ"),
        ("called", "Заказ согласован"),
        ("in_process", "Заказ отдан заказчику"),
        ("closed", "Заказ закрыт"),
    ]

    status = models.CharField(max_length=100, choices=STATUS_CHOICES, verbose_name="Статус")

    @property
    def reserved_days(self):
        timedelta = self.end_date - self.start_date
        addidational_day = 1 if timedelta.total_seconds() % 86400 > 0 else 0
        return timedelta.days + addidational_day

    def clean(self):
        if (self.end_date.date() - self.start_date.date()).days < 1:
            raise ValidationError("Минимальный срок бронирования, должен быть не меньше 1 дня.")

    def __str__(self):
        return "Заказ №{} | Сумма заказа: {}".format(self.id, self.price)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class ProductsToOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="product_in_orders")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name="products_in_order")
    count = models.PositiveIntegerField(verbose_name="Количество товара")

    def __str__(self):
        return "{} | {}".format(self.product, self.order)

    class Meta:
        verbose_name = "Товар к заказу"
        verbose_name_plural = "Товары к заказам"
