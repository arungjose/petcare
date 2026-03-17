from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .forms import BuyerRegistrationForm, SellerRegistrationForm, CustomLoginForm, BuyerProfileUpdateForm, SellerProfileUpdateForm
from .models import User, SellerProfile


def choose_register(request):
    return render(request, 'accounts/choose_register.html')


def buyer_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to BARN, {user.first_name}! Start exploring pets.")
            return redirect('home')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'accounts/buyer_register.html', {'form': form})


def seller_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to BARN! Your seller profile is under review. You can start listing pets once approved.")
            return redirect('seller_dashboard')
    else:
        form = SellerRegistrationForm()
    return render(request, 'accounts/seller_register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            if user.is_seller():
                return redirect('seller_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You've been logged out. See you soon!")
    return redirect('home')


@login_required
def buyer_dashboard(request):
    if not request.user.is_buyer():
        return redirect('seller_dashboard')
    profile = getattr(request.user, 'buyer_profile', None)
    return render(request, 'accounts/buyer_dashboard.html', {'profile': profile})


@login_required
def seller_dashboard(request):
    if not request.user.is_seller():
        return redirect('buyer_dashboard')
    seller_profile = getattr(request.user, 'seller_profile', None)
    pets = request.user.listed_pets.all() if hasattr(request.user, 'listed_pets') else []
    products = request.user.products.all() if hasattr(request.user, 'products') else []
    return render(request, 'accounts/seller_dashboard.html', {
        'seller_profile': seller_profile,
        'pets': pets,
        'products': products,
    })


@login_required
def edit_profile(request):
    if request.user.is_seller():
        profile = get_object_or_404(SellerProfile, user=request.user)
        FormClass = SellerProfileUpdateForm
    else:
        from .models import BuyerProfile
        profile, _ = BuyerProfile.objects.get_or_create(user=request.user)
        FormClass = BuyerProfileUpdateForm

    if request.method == 'POST':
        form = FormClass(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            if request.user.is_seller():
                return redirect('seller_dashboard')
            return redirect('buyer_dashboard')
    else:
        form = FormClass(instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})


def seller_public_profile(request, slug):
    seller = get_object_or_404(SellerProfile, slug=slug)
    pets = seller.user.listed_pets.filter(is_available=True) if hasattr(seller.user, 'listed_pets') else []
    products = seller.user.products.filter(is_available=True) if hasattr(seller.user, 'products') else []
    reviews = seller.reviews.all().order_by('-created_at')
    return render(request, 'accounts/seller_public.html', {
        'seller': seller,
        'pets': pets,
        'products': products,
        'reviews': reviews,
    })
