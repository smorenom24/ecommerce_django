from django.urls import path
from .views import login_page,register_user,activate_email,add_to_cart,cart,remove_cart,remove_coupon

app_name = 'account'

urlpatterns = [
    path("login/", login_page, name='login'),
    path("register/", register_user, name='register'),
    path("activate/<email_token>/", activate_email, name='activate'),
    path("cart/", cart, name='cart'),
    path('add-to-cart/<uid>/', add_to_cart, name='add-to-cart'),
    path('remove-cart/<uid>/', remove_cart, name='remove-cart'),
    path('remove-coupon/<cart_uid>/', remove_coupon, name='remove-coupon'),
]
#path('cart/', cart, name="cart"),
