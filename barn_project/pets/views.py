from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Pet, PetCategory, PetBreed, PetImage, PetInquiry
from .forms import PetListingForm, PetImageFormSet, PetInquiryForm


def pet_list(request):
    pets = Pet.objects.filter(is_available=True).select_related('category', 'breed', 'seller')
    categories = PetCategory.objects.all()

    # Filters
    category_slug = request.GET.get('category')
    listing_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('q')
    gender = request.GET.get('gender')

    if category_slug:
        pets = pets.filter(category__slug=category_slug)
    if listing_type:
        pets = pets.filter(listing_type__in=[listing_type, 'both'])
    if min_price:
        pets = pets.filter(price__gte=min_price)
    if max_price:
        pets = pets.filter(price__lte=max_price)
    if search:
        pets = pets.filter(
            Q(name__icontains=search) |
            Q(breed__name__icontains=search) |
            Q(category__name__icontains=search) |
            Q(description__icontains=search)
        )
    if gender:
        pets = pets.filter(gender=gender)

    context = {
        'pets': pets,
        'categories': categories,
        'selected_category': category_slug,
        'selected_type': listing_type,
        'search_query': search,
    }
    return render(request, 'pets/pet_list.html', context)


def pet_detail(request, slug):
    pet = get_object_or_404(Pet, slug=slug, is_available=True)
    pet.views_count += 1
    pet.save(update_fields=['views_count'])

    inquiry_form = PetInquiryForm()
    if request.method == 'POST':
        inquiry_form = PetInquiryForm(request.POST)
        if inquiry_form.is_valid():
            inquiry = inquiry_form.save(commit=False)
            inquiry.pet = pet
            if request.user.is_authenticated:
                inquiry.buyer = request.user
            inquiry.save()
            messages.success(request, "Your inquiry has been sent! The seller will contact you soon.")
            return redirect('pet_detail', slug=slug)

    related_pets = Pet.objects.filter(
        category=pet.category, is_available=True
    ).exclude(pk=pet.pk)[:4]

    seller_profile = getattr(pet.seller, 'seller_profile', None)

    context = {
        'pet': pet,
        'inquiry_form': inquiry_form,
        'related_pets': related_pets,
        'seller_profile': seller_profile,
    }
    return render(request, 'pets/pet_detail.html', context)


def adoption_list(request):
    pets = Pet.objects.filter(
        is_available=True,
        listing_type__in=['adoption', 'both']
    ).select_related('category', 'breed', 'seller')
    categories = PetCategory.objects.all()

    category_slug = request.GET.get('category')
    if category_slug:
        pets = pets.filter(category__slug=category_slug)

    return render(request, 'pets/adoption_list.html', {
        'pets': pets,
        'categories': categories,
        'selected_category': category_slug,
    })


@login_required
def add_pet(request):
    if not request.user.is_seller():
        messages.error(request, "Only registered sellers can list pets.")
        return redirect('pet_list')

    if request.method == 'POST':
        form = PetListingForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.seller = request.user
            pet.save()

            # Handle multiple images
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                PetImage.objects.create(
                    pet=pet,
                    image=image,
                    is_primary=(i == 0)
                )

            messages.success(request, f"'{pet.name}' has been listed successfully!")
            return redirect('seller_dashboard')
    else:
        form = PetListingForm()

    return render(request, 'pets/add_pet.html', {'form': form})


@login_required
def edit_pet(request, slug):
    pet = get_object_or_404(Pet, slug=slug, seller=request.user)
    if request.method == 'POST':
        form = PetListingForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for i, image in enumerate(images):
                PetImage.objects.create(pet=pet, image=image)
            messages.success(request, "Pet listing updated!")
            return redirect('seller_dashboard')
    else:
        form = PetListingForm(instance=pet)
    return render(request, 'pets/edit_pet.html', {'form': form, 'pet': pet})


@login_required
def delete_pet(request, slug):
    pet = get_object_or_404(Pet, slug=slug, seller=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, "Pet listing removed.")
        return redirect('seller_dashboard')
    return render(request, 'pets/delete_pet.html', {'pet': pet})


def category_pets(request, slug):
    category = get_object_or_404(PetCategory, slug=slug)
    pets = Pet.objects.filter(category=category, is_available=True)
    return render(request, 'pets/category_pets.html', {'category': category, 'pets': pets})


def load_breeds(request):
    category_id = request.GET.get('category')
    breeds = PetBreed.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'pets/breed_dropdown_list_options.html', {'breeds': breeds})
