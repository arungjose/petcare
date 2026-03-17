from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import ServiceCategory, Service, ServiceBooking, Testimonial
from .forms import ServiceBookingForm


def services_home(request):
    categories = ServiceCategory.objects.prefetch_related('services').all()
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    return render(request, 'services/services_home.html', {
        'categories': categories,
        'testimonials': testimonials,
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_available=True)
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            if request.user.is_authenticated:
                booking.customer = request.user
            booking.save()
            messages.success(request, f"Booking confirmed for {service.name}! We'll contact you shortly to confirm.")
            return redirect('service_detail', slug=slug)
    else:
        form = ServiceBookingForm()
        if request.user.is_authenticated:
            form.initial = {
                'customer_name': request.user.get_full_name() or request.user.username,
                'customer_email': request.user.email,
                'customer_phone': request.user.phone,
            }

    related = Service.objects.filter(category=service.category, is_available=True).exclude(pk=service.pk)[:3]
    return render(request, 'services/service_detail.html', {
        'service': service,
        'form': form,
        'related': related,
    })


def grooming(request):
    category = ServiceCategory.objects.filter(slug='grooming').first()
    services = Service.objects.filter(category__slug='grooming', is_available=True)
    return render(request, 'services/category_page.html', {
        'category': category,
        'services': services,
        'page_title': 'Grooming Services',
        'page_icon': '✂️',
    })


def veterinary(request):
    category = ServiceCategory.objects.filter(slug='veterinary').first()
    services = Service.objects.filter(category__slug='veterinary', is_available=True)
    return render(request, 'services/category_page.html', {
        'category': category,
        'services': services,
        'page_title': 'Veterinary Care',
        'page_icon': '🩺',
    })


def training(request):
    category = ServiceCategory.objects.filter(slug='training').first()
    services = Service.objects.filter(category__slug='training', is_available=True)
    return render(request, 'services/category_page.html', {
        'category': category,
        'services': services,
        'page_title': 'Pet Training',
        'page_icon': '🏅',
    })


def boarding(request):
    category = ServiceCategory.objects.filter(slug='boarding').first()
    services = Service.objects.filter(category__slug='boarding', is_available=True)
    return render(request, 'services/category_page.html', {
        'category': category,
        'services': services,
        'page_title': 'Boarding & Sitting',
        'page_icon': '🏠',
    })
