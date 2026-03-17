from django.db import models
from django.utils.text import slugify
from accounts.models import User


class StoreCategory(models.Model):
    SUPPLY = 'supply'
    ACCESSORY = 'accessory'
    TYPE_CHOICES = [(SUPPLY, 'Supply'), (ACCESSORY, 'Accessory')]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=SUPPLY)
    icon = models.CharField(max_length=10, default='🛒')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Store Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    category = models.ForeignKey(StoreCategory, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    brand = models.CharField(max_length=100, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                          help_text="Original price before discount")
    stock = models.PositiveIntegerField(default=0)
    weight = models.CharField(max_length=50, blank=True, help_text="e.g., '500g', '2kg'")
    suitable_for = models.CharField(max_length=200, blank=True, help_text="e.g., 'Dogs, Cats'")
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total(self):
        return sum(item.subtotal for item in self.items.all())

    def get_item_count(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart {self.session_key}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        if self.product:
            return self.product.price * self.quantity
        if self.pet:
            return (self.pet.price or 0) * self.quantity
        return 0

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"


class Order(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSING = 'processing'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSING, 'Processing'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_DELIVERED, 'Delivered'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    order_number = models.CharField(max_length=20, unique=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random, string
            self.order_number = 'BARN-' + ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    pet = models.ForeignKey('pets.Pet', on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.price * self.quantity
