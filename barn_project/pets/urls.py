from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_list, name='pet_list'),
    path('adopt/', views.adoption_list, name='adoption_list'),
    path('add/', views.add_pet, name='add_pet'),
    path('category/<slug:slug>/', views.category_pets, name='category_pets'),
    path('ajax/load-breeds/', views.load_breeds, name='ajax_load_breeds'),
    path('<slug:slug>/', views.pet_detail, name='pet_detail'),
    path('<slug:slug>/edit/', views.edit_pet, name='edit_pet'),
    path('<slug:slug>/delete/', views.delete_pet, name='delete_pet'),
]
