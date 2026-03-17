from django import forms
from .models import Order, Product


class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Full name'}))
    customer_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}))
    customer_phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': '+91 XXXXX XXXXX'}))
    shipping_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Street address, apartment, etc.'}))
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'brand', 'short_description', 'description', 'price', 'original_price', 'stock', 'suitable_for', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'suitable_for': forms.TextInput(attrs={'placeholder': 'e.g., Dogs, Cats'}),
        }
