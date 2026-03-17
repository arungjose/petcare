from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SellerProfile, BuyerProfile, SellerReview


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('BARN Profile', {'fields': ('role', 'phone', 'profile_picture', 'bio')}),
    )


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'city', 'verification_status', 'created_at')
    list_filter = ('verification_status', 'country')
    search_fields = ('business_name', 'user__username', 'breeder_license_number')
    actions = ['approve_sellers', 'reject_sellers']

    def approve_sellers(self, request, queryset):
        from django.utils import timezone
        queryset.update(verification_status='approved', verified_at=timezone.now())
        self.message_user(request, f"{queryset.count()} seller(s) approved.")
    approve_sellers.short_description = "Approve selected sellers"

    def reject_sellers(self, request, queryset):
        queryset.update(verification_status='rejected')
        self.message_user(request, f"{queryset.count()} seller(s) rejected.")
    reject_sellers.short_description = "Reject selected sellers"


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'created_at')


@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ('seller', 'buyer', 'rating', 'created_at')
