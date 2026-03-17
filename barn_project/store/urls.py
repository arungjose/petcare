from django.urls import path
from . import views

urlpatterns = [
    path('', views.store_home, name='store_home'),
    path('products/', views.product_list, name='product_list'),
    path('accessories/', views.accessories, name='accessories'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/add/pet/<int:pet_id>/', views.add_to_cart, name='add_to_cart_pet'),
    path('cart/buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/buy/pet/<int:pet_id>/', views.buy_now, name='buy_now_pet'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/<str:order_number>/success/', views.order_success, name='order_success'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-accessory/', views.add_accessory, name='add_accessory'),
    path('edit-accessory/<int:pk>/', views.edit_accessory, name='edit_accessory'),
]
