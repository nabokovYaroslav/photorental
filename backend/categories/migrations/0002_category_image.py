# Generated by Django 3.2.13 on 2022-06-06 22:59

import categories.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to=categories.models.Category.upload_to, verbose_name='Фотография'),
        ),
    ]
