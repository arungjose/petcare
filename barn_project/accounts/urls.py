from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.choose_register, name='choose_register'),
    path('register/buyer/', views.buyer_register, name='buyer_register'),
    path('register/seller/', views.seller_register, name='seller_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/buyer/', views.buyer_dashboard, name='buyer_dashboard'),
    path('dashboard/seller/', views.seller_dashboard, name='seller_dashboard'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('seller/<slug:slug>/', views.seller_public_profile, name='seller_public_profile'),
]
