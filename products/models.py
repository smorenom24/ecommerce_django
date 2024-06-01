from django.db import models

from base.models import BaseModel
from django.utils.text import slugify


# Create your models here.

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to='categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.color_name + ' - $' + str(self.price)


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    product_description = models.TextField()
    price = models.PositiveIntegerField()
    product_stock = models.PositiveIntegerField(default=0)
    color_variant = models.ManyToManyField(ColorVariant, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def get_product_price_by_color(self, color):

        color_selected = self.color_variant.get(
            color_name=color
        )
        print(f"color: {color_selected}")
        final_amount = self.price + color_selected.price
        print(f"final_amount: {final_amount}")
        return final_amount


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=0)
    minimum_amount = models.IntegerField(default=30000)

    def __str__(self):
        return self.coupon_code
