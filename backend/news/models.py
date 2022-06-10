import os

from django.db import models
from django.utils import timezone


class New(models.Model):
    def upload_to(self, file):
        name, ext = os.path.splitext(file)
        path = "images/news/"
        datetime = timezone.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        output_path = '{}{}-{}{}'.format(path, name, datetime, ext)
        return output_path

    name = models.CharField(max_length=100, verbose_name="Название новости")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to=upload_to, max_length=255, verbose_name="Фотография")
    created_at = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"