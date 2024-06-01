from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

#djando messages:
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, Profile, Cart, CartItems
from products.models import Product, ColorVariant, Coupon


# Create your views here.


def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
            username=email
        )
        if not user_obj.exists():
            messages.error(request, "Account not found.")
            return HttpResponseRedirect(request.path_info)
        if not user_obj[0].profile.is_email_verified:
            messages.error(request, "Your account is not verified.")
            return HttpResponseRedirect(request.path_info)
        user_obj = authenticate(
            username=email,
            password=password
        )
        if user_obj:
            login(request, user_obj)
            return redirect('/')

        messages.error(request, "Invalid credentials.")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')


def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
            username=email
        )
        if user_obj.exists():
            messages.warning(request, "Email is already taken.")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email
        )
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request, "Account created. An email has been sent on your email.")
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/register.html')


def activate_email(request, email_token):
    try:
        profile = Profile.objects.get(
            email_token=email_token
        )
        profile.is_email_verified = True
        profile.save()
        return redirect('/')
    except Exception as e:
        print(e)
        return HttpResponse('An error has occurred')


def cart(request):
    cart_to_buy = None
    cart_items = None
    try:
        cart_to_buy = Cart.objects.get(
            is_paid=False,
            user=request.user)
        cart_items = CartItems.objects.filter(cart=cart_to_buy)
    except Exception as e:
        print(e)
    if request.method == "POST":
        total_amount = cart_to_buy.get_cart_total()
        coupon_post = request.POST.get('coupon')
        coupon_to_use = Coupon.objects.filter(
            coupon_code=coupon_post
        )
        if not coupon_to_use.exists():
            messages.warning(request, "Invalid Coupon code.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart_to_buy.coupon:
            messages.warning(request, "Coupon code is already taken.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if cart_to_buy.get_cart_total() < coupon_to_use[0].minimum_amount:
            messages.warning(request, f"Amount should be greater than ${coupon_to_use[0].minimum_amount}.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if coupon_to_use[0].is_expired:
            messages.warning(request, f"Coupon expired.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        cart_to_buy.coupon = coupon_to_use[0]
        cart_to_buy.save()
        messages.success(request, "Coupon applied.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'cart': cart_to_buy,
        'cart_items': cart_items
    }
    return render(request, 'accounts/cart.html', context)


def remove_coupon(request, cart_uid):
    cart_selected = Cart.objects.get(uid=cart_uid)
    cart_selected.coupon = None
    cart_selected.save()
    messages.success(request, "Coupon removed.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request, uid):
    try:
        cart_item = CartItems.objects.get(
            uid=uid
        )
        cart_item.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_to_cart(request, uid):
    color = request.GET.get('color')
    product = Product.objects.get(uid=uid)
    user = request.user
    cart_to_buy, _ = Cart.objects.get_or_create(
        user=user,
        is_paid=False
    )
    cart_items = CartItems.objects.create(
        cart=cart_to_buy,
        products=product,
    )
    if color:
        color_variant = product.color_variant.get(color_name=color)
        cart_items.color_variant = color_variant
        cart_items.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
