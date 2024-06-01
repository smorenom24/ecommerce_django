# Generated by Django 5.0.6 on 2024-05-31 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_productimage_color_variant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colorvariant',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='color_variant',
        ),
        migrations.AddField(
            model_name='product',
            name='color_variant',
            field=models.ManyToManyField(blank=True, to='products.colorvariant'),
        ),
    ]
