from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from pets.models import Pet, PetCategory
from services.models import Service, ServiceCategory
from store.models import Product


def home(request):
    featured_pets = Pet.objects.filter(is_available=True).select_related('category', 'breed')[:8]
    categories = PetCategory.objects.all()
    adoption_pets = Pet.objects.filter(is_available=True, listing_type__in=['adoption', 'both'])[:4]
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:4]
    service_cats = ServiceCategory.objects.prefetch_related('services').all()[:4]

    context = {
        'featured_pets': featured_pets,
        'categories': categories,
        'adoption_pets': adoption_pets,
        'featured_products': featured_products,
        'service_cats': service_cats,
    }
    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'General Inquiry')
        message_body = request.POST.get('message')

        if name and email and message_body:
            messages.success(request, f"Thank you, {name}! We've received your message and will get back to you soon.")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, 'core/contact.html')
