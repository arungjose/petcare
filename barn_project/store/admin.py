from django.contrib import admin
from .models import StoreCategory, Product, Cart, CartItem, Order, OrderItem


@admin.register(StoreCategory)
class StoreCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'price', 'stock', 'is_featured', 'is_available')
    list_filter = ('category', 'is_featured', 'is_available')
    list_editable = ('is_featured', 'is_available', 'stock')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'brand')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)
    inlines = [OrderItemInline]
