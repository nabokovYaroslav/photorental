import os

from django.db import models
from django.utils import timezone


class Studio(models.Model):
    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/studios/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    name = models.CharField(max_length=100, verbose_name="Название студии")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена в час")
    image = models.ImageField(upload_to=upload_to, max_length=255, verbose_name="Фотография")
    phone = models.CharField(max_length=14, verbose_name="Телефон")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Студия"
        verbose_name_plural = 'Студии'