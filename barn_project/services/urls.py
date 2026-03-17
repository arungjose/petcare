from django.urls import path
from . import views

urlpatterns = [
    path('', views.services_home, name='services_home'),
    path('grooming/', views.grooming, name='grooming'),
    path('veterinary/', views.veterinary, name='veterinary'),
    path('training/', views.training, name='training'),
    path('boarding/', views.boarding, name='boarding'),
    path('<slug:slug>/', views.service_detail, name='service_detail'),
]
