from django.db import models
from django.utils.text import slugify
from accounts.models import User


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=10, default='🐾')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Service Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., '2 hours', '1 day'")
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    includes = models.TextField(blank=True, help_text="Comma-separated list of what's included")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_includes_list(self):
        return [item.strip() for item in self.includes.split(',') if item.strip()]

    def __str__(self):
        return self.name


class ServiceBooking(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_bookings', null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=50)
    pet_breed = models.CharField(max_length=100, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} - {self.customer_name} ({self.appointment_date})"


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.rating}★"
