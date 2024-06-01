from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Product, ColorVariant, Coupon


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile', blank=True, null=True)

    def get_cart_count(self):
        cart = Cart.objects.get(
            user=self.user,
            is_paid=False
        )
        return CartItems.objects.filter(cart=cart).count()


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email_token = str(uuid.uuid4())
            Profile.objects.create(
                user=instance,
                email_token=email_token,
                is_email_verified=False
            )
            email = instance.email
            print(f"email a confirmar: {email}")
            send_account_activation_email(email, email_token)
    except Exception as e:
        print(e)


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    is_paid = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True, blank=True, related_name='carts')
    """def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.color_variant:
                price.append(cart_item.color_variant.price)
        print(price)
        return sum(price)"""

    def get_cart_total(self):
        cart_items = CartItems.objects.filter(
            cart=self
        )
        price=[]
        for cart_item in cart_items:
            price.append(cart_item.products.price)
            if cart_item.color_variant:
                price.append(cart_item.color_variant.price)
        total = sum(price)
        if self.coupon and self.coupon.minimum_amount < total:
            print(f"Discount: {self.coupon.discount_price}")
            total = int(total * (1 - self.coupon.discount_price/100))
        return total


class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    products = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='cart_items')
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='cart_items_color')

    def __str__(self):
        return "ID_carro: " + str(self.cart.uid) + " - " + str(self.products) + " - " + str(self.color_variant)

    def get_product_price(self):
        price = [self.products.price]

        if self.color_variant:
            color_variant_price = self.color_variant.price
            price.append(color_variant_price)
        return sum(price)
