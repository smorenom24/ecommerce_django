from django.shortcuts import render

from accounts.models import Cart
from products.models import Product, ProductImage, ColorVariant
from django.shortcuts import redirect

# Create your views here.
def get_products(request, slug):
    product = Product.objects.get(slug=slug)
    context = {'product': product}
    color_get = request.GET.get('color')
    if color_get:
        price = product.get_product_price_by_color(color_get)
        context['selected_color'] = color_get
        context['updated_price'] = price
    return render(request, 'product/product.html', context)

