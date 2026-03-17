from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    ROLE_BUYER = 'buyer'
    ROLE_SELLER = 'seller'
    ROLE_OPERATOR = 'operator'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_BUYER, 'Buyer'),
        (ROLE_SELLER, 'Seller / Breeder'),
        (ROLE_OPERATOR, 'Operator'),
        (ROLE_ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_BUYER)
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_seller(self):
        return self.role == self.ROLE_SELLER

    def is_operator(self):
        return self.role == self.ROLE_OPERATOR or self.is_staff

    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def can_list_products(self):
        return self.role in [self.ROLE_SELLER, self.ROLE_OPERATOR, self.ROLE_ADMIN] or self.is_staff or self.is_superuser

    def is_buyer(self):
        return self.role == self.ROLE_BUYER

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class SellerProfile(models.Model):
    VERIFICATION_PENDING = 'pending'
    VERIFICATION_APPROVED = 'approved'
    VERIFICATION_REJECTED = 'rejected'
    VERIFICATION_CHOICES = [
        (VERIFICATION_PENDING, 'Pending Review'),
        (VERIFICATION_APPROVED, 'Approved'),
        (VERIFICATION_REJECTED, 'Rejected'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    # License & Verification
    breeder_license_number = models.CharField(max_length=100, verbose_name="Breeder/Seller License Number")
    license_document = models.FileField(upload_to='licenses/', blank=True, null=True, verbose_name="License Document (PDF/Image)")
    government_id = models.FileField(upload_to='government_ids/', blank=True, null=True, verbose_name="Government ID")
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default=VERIFICATION_PENDING)
    verified_at = models.DateTimeField(null=True, blank=True)

    # Business Address
    street_address = models.CharField(max_length=255, verbose_name="Street Address")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, verbose_name="State / Province")
    postal_code = models.CharField(max_length=20, verbose_name="Postal / ZIP Code")
    country = models.CharField(max_length=100, default='India')

    # Contact
    business_phone = models.CharField(max_length=20, verbose_name="Business Phone")
    business_email = models.EmailField(verbose_name="Business Email")
    website = models.URLField(blank=True, verbose_name="Website URL")

    # Business Details
    years_in_business = models.PositiveIntegerField(default=0, verbose_name="Years in Business")
    specialization = models.CharField(max_length=255, blank=True, verbose_name="Specialization (e.g., Golden Retrievers, Exotic Birds)")
    kennel_club_membership = models.CharField(max_length=200, blank=True, verbose_name="Kennel Club / Association Membership")
    about_business = models.TextField(verbose_name="About Your Business")

    # Social / Media
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)

    # Ratings
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.business_name)
            # ensure uniqueness
            base_slug = self.slug
            counter = 1
            while SellerProfile.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def full_address(self):
        return f"{self.street_address}, {self.city}, {self.state} {self.postal_code}, {self.country}"

    def __str__(self):
        return f"{self.business_name} - {self.user.username}"


class BuyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')
    preferred_pet_types = models.CharField(max_length=200, blank=True)
    newsletter_subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buyer: {self.user.username}"


class SellerReview(models.Model):
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('seller', 'buyer')

    def __str__(self):
        return f"Review by {self.buyer.username} for {self.seller.business_name}"
