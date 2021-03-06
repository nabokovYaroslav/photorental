# Generated by Django 3.2.13 on 2022-06-02 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enumvalue',
            name='enum_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enum_group_values', to='products.enumgroup', verbose_name='Группа выбора'),
        ),
        migrations.AlterUniqueTogether(
            name='value',
            unique_together={('attribute', 'product')},
        ),
    ]
