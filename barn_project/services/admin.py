from django.contrib import admin
from .models import ServiceCategory, Service, ServiceBooking, Testimonial


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'duration', 'is_available')
    list_filter = ('category', 'is_available')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'customer_name', 'appointment_date', 'status', 'created_at')
    list_filter = ('status', 'appointment_date')
    list_editable = ('status',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'rating', 'is_featured')
    list_editable = ('is_featured',)
