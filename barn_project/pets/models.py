from django.db import models
from django.utils.text import slugify
from accounts.models import User


class PetCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='🐾')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Pet Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PetBreed(models.Model):
    category = models.ForeignKey(PetCategory, on_delete=models.CASCADE, related_name='breeds')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Pet(models.Model):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]

    LISTING_SALE = 'sale'
    LISTING_ADOPTION = 'adoption'
    LISTING_BOTH = 'both'
    LISTING_CHOICES = [
        (LISTING_SALE, 'For Sale'),
        (LISTING_ADOPTION, 'For Adoption'),
        (LISTING_BOTH, 'Sale or Adoption'),
    ]

    AGE_UNIT_WEEKS = 'weeks'
    AGE_UNIT_MONTHS = 'months'
    AGE_UNIT_YEARS = 'years'
    AGE_UNIT_CHOICES = [
        (AGE_UNIT_WEEKS, 'Weeks'),
        (AGE_UNIT_MONTHS, 'Months'),
        (AGE_UNIT_YEARS, 'Years'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_pets')
    category = models.ForeignKey(PetCategory, on_delete=models.CASCADE, related_name='pets')
    breed = models.ForeignKey(PetBreed, on_delete=models.SET_NULL, null=True, blank=True, related_name='pets')

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    age_value = models.PositiveIntegerField(default=1)
    age_unit = models.CharField(max_length=10, choices=AGE_UNIT_CHOICES, default=AGE_UNIT_MONTHS)
    color = models.CharField(max_length=100, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    listing_type = models.CharField(max_length=20, choices=LISTING_CHOICES, default=LISTING_SALE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                 help_text="Leave blank for adoption-only listings")

    # Health records
    is_vaccinated = models.BooleanField(default=False)
    is_dewormed = models.BooleanField(default=False)
    is_microchipped = models.BooleanField(default=False)
    is_neutered = models.BooleanField(default=False)
    health_certificate = models.FileField(upload_to='health_certs/', blank=True, null=True)
    health_notes = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)

    is_available = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.category.name}")
            self.slug = base_slug
            counter = 1
            while Pet.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    @property
    def age_display(self):
        return f"{self.age_value} {self.age_unit}"

    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    def __str__(self):
        return f"{self.name} - {self.breed or self.category.name}"


class PetImage(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pets/')
    is_primary = models.BooleanField(default=False)
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.pet.name}"


class PetInquiry(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='inquiries')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries', null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)

    def __str__(self):
        return f"Inquiry for {self.pet.name} from {self.name}"
