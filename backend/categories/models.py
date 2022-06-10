import os

from django.db import models
from django.utils import timezone


class Category(models.Model):
    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/categories/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    name = models.CharField(max_length=100, unique=True, verbose_name="Категория")
    image = models.ImageField(upload_to=upload_to, max_length=255, verbose_name="Фотография")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"