from django.contrib import admin
from .models import PetCategory, PetBreed, Pet, PetImage, PetInquiry


@admin.register(PetCategory)
class PetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(PetBreed)
class PetBreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)


class PetImageInline(admin.TabularInline):
    model = PetImage
    extra = 1


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'breed', 'seller', 'listing_type', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'listing_type', 'is_available', 'gender')
    search_fields = ('name', 'seller__username', 'breed__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PetImageInline]


@admin.register(PetInquiry)
class PetInquiryAdmin(admin.ModelAdmin):
    list_display = ('pet', 'name', 'email', 'created_at', 'is_responded')
    list_filter = ('is_responded',)
