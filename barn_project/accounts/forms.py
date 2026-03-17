from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, SellerProfile, BuyerProfile


class BuyerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, initial='India', required=False)
    newsletter_subscribed = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        user.role = User.ROLE_BUYER
        if commit:
            user.save()
            BuyerProfile.objects.create(
                user=user,
                date_of_birth=self.cleaned_data.get('date_of_birth'),
                city=self.cleaned_data.get('city', ''),
                state=self.cleaned_data.get('state', ''),
                country=self.cleaned_data.get('country', 'India'),
                newsletter_subscribed=self.cleaned_data.get('newsletter_subscribed', True),
            )
        return user


class SellerRegistrationForm(UserCreationForm):
    # Personal Info
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=20, required=True, label="Personal Phone")

    # Business Info
    business_name = forms.CharField(max_length=200, required=True, label="Business / Kennel Name")
    breeder_license_number = forms.CharField(max_length=100, required=True, label="Breeder / Seller License Number")
    license_document = forms.FileField(required=False, label="Upload License Document (PDF/Image)",
                                        widget=forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}))
    government_id = forms.FileField(required=False, label="Upload Government ID",
                                     widget=forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}))

    # Business Address
    street_address = forms.CharField(max_length=255, required=True, label="Street Address")
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True, label="State / Province")
    postal_code = forms.CharField(max_length=20, required=True, label="Postal / ZIP Code")
    country = forms.CharField(max_length=100, initial='India', required=True)

    # Contact
    business_phone = forms.CharField(max_length=20, required=True, label="Business Phone")
    business_email = forms.EmailField(required=True, label="Business Email")
    website = forms.URLField(required=False, label="Website URL (optional)")

    # Business Details
    years_in_business = forms.IntegerField(min_value=0, required=True, label="Years in Business")
    specialization = forms.CharField(max_length=255, required=False,
                                      label="Specialization (e.g., Golden Retrievers, Exotic Birds)")
    kennel_club_membership = forms.CharField(max_length=200, required=False,
                                              label="Kennel Club / Association Membership (if any)")
    about_business = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True,
        label="Tell us about your breeding/selling experience"
    )

    # Social
    instagram = forms.URLField(required=False, label="Instagram URL (optional)")
    facebook = forms.URLField(required=False, label="Facebook URL (optional)")

    # Agreement
    agree_terms = forms.BooleanField(
        required=True,
        label="I agree to BARN's Seller Terms & Conditions and confirm all information provided is accurate."
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        user.role = User.ROLE_SELLER
        if commit:
            user.save()
            SellerProfile.objects.create(
                user=user,
                business_name=self.cleaned_data['business_name'],
                breeder_license_number=self.cleaned_data['breeder_license_number'],
                license_document=self.cleaned_data.get('license_document'),
                government_id=self.cleaned_data.get('government_id'),
                street_address=self.cleaned_data['street_address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                postal_code=self.cleaned_data['postal_code'],
                country=self.cleaned_data.get('country', 'India'),
                business_phone=self.cleaned_data['business_phone'],
                business_email=self.cleaned_data['business_email'],
                website=self.cleaned_data.get('website', ''),
                years_in_business=self.cleaned_data.get('years_in_business', 0),
                specialization=self.cleaned_data.get('specialization', ''),
                kennel_club_membership=self.cleaned_data.get('kennel_club_membership', ''),
                about_business=self.cleaned_data['about_business'],
                instagram=self.cleaned_data.get('instagram', ''),
                facebook=self.cleaned_data.get('facebook', ''),
            )
        return user


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


class BuyerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ('date_of_birth', 'address', 'city', 'state', 'country', 'preferred_pet_types', 'newsletter_subscribed')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class SellerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = (
            'business_name', 'street_address', 'city', 'state', 'postal_code', 'country',
            'business_phone', 'business_email', 'website',
            'years_in_business', 'specialization', 'kennel_club_membership',
            'about_business', 'instagram', 'facebook',
        )
