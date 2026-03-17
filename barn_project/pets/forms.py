from django import forms
from .models import Pet, PetInquiry


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PetListingForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        required=False,
        label="Upload Pet Photos"
    )

    class Meta:
        model = Pet
        fields = [
            'name', 'category', 'breed', 'gender', 'age_value', 'age_unit',
            'color', 'weight_kg', 'description', 'listing_type', 'price', 'quantity',
            'is_vaccinated', 'is_dewormed', 'is_microchipped', 'is_neutered',
            'health_certificate', 'health_notes', 'is_available',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'health_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].help_text = "Required for Sale listings. Leave blank for Adoption-only."


class PetImageFormSet(forms.BaseInlineFormSet):
    pass


class PetInquiryForm(forms.ModelForm):
    class Meta:
        model = PetInquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': "Hi, I'm interested in this pet..."}),
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone (optional)'}),
        }
