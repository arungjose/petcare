from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import StoreCategory, Product, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm, ProductForm


def store_home(request):
    categories = StoreCategory.objects.prefetch_related('products').all()
    featured = Product.objects.filter(is_featured=True, is_available=True)[:8]
    supplies = StoreCategory.objects.filter(category_type='supply')
    accessories = StoreCategory.objects.filter(category_type='accessory')
    return render(request, 'store/store_home.html', {
        'categories': categories,
        'featured': featured,
        'supplies': supplies,
        'accessories': accessories,
    })


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = StoreCategory.objects.all()

    cat_slug = request.GET.get('category')
    cat_type = request.GET.get('type')
    search = request.GET.get('q')
    sort = request.GET.get('sort', '-created_at')

    if cat_slug:
        products = products.filter(category__slug=cat_slug)
    if cat_type:
        products = products.filter(category__category_type=cat_type)
    if search:
        products = products.filter(Q(name__icontains=search) | Q(brand__icontains=search) | Q(description__icontains=search))

    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        '-created_at': '-created_at',
    }
    products = products.order_by(sort_map.get(sort, '-created_at'))

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_cat': cat_slug,
        'selected_type': cat_type,
        'search_query': search,
        'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related = Product.objects.filter(category=product.category, is_available=True).exclude(pk=product.pk)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related': related})


def accessories(request):
    products = Product.objects.filter(category__category_type='accessory', is_available=True)
    categories = StoreCategory.objects.filter(category_type='accessory')
    return render(request, 'store/product_list.html', {
        'products': products, 'categories': categories,
        'page_title': 'Premium Accessories', 'selected_type': 'accessory',
    })


def _get_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_view(request):
    cart = _get_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def add_to_cart(request, product_id=None, pet_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id, is_available=True)
        pet = None
    else:
        from pets.models import Pet
        pet = get_object_or_404(Pet, id=pet_id, is_available=True)
        product = None
    
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1)) if request.method == 'POST' else int(request.GET.get('quantity', 1))
        
    if product:
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item_name = product.name
    else:
        item, created = CartItem.objects.get_or_create(cart=cart, pet=pet)
        item_name = pet.name

    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()
    
    messages.success(request, f"'{item_name}' (x{qty}) added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'store_home'))


def buy_now(request, product_id=None, pet_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id, is_available=True)
        pet = None
    else:
        from pets.models import Pet
        pet = get_object_or_404(Pet, id=pet_id, is_available=True)
        product = None
        
    cart = _get_cart(request)
    qty = int(request.POST.get('quantity', 1)) if request.method == 'POST' else int(request.GET.get('quantity', 1))
        
    if product:
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    else:
        item, created = CartItem.objects.get_or_create(cart=cart, pet=pet)

    if not created:
        item.quantity += qty
    else:
        item.quantity = qty
    item.save()
    
    return redirect('checkout')


def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=_get_cart(request))
    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect('cart_view')


def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=_get_cart(request))
    qty = int(request.POST.get('quantity', 1))
    if qty < 1:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect('cart_view')


def checkout(request):
    cart = _get_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('store_home')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer_name=form.cleaned_data['customer_name'],
                customer_email=form.cleaned_data['customer_email'],
                customer_phone=form.cleaned_data['customer_phone'],
                shipping_address=form.cleaned_data['shipping_address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                total_amount=cart.get_total(),
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    pet=item.pet,
                    product_name=item.product.name if item.product else item.pet.name,
                    price=item.product.price if item.product else item.pet.price,
                    quantity=item.quantity,
                )
            cart.items.all().delete()
            messages.success(request, f"Order {order.order_number} placed successfully! We'll deliver soon.")
            return redirect('order_success', order_number=order.order_number)
    else:
        form = CheckoutForm()
        if request.user.is_authenticated:
            form.initial = {
                'customer_name': request.user.get_full_name(),
                'customer_email': request.user.email,
                'customer_phone': request.user.phone,
            }

    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def add_accessory(request):
    if not request.user.can_list_products():
        messages.error(request, "Only verified sellers, operators, or admins can list products.")
        return redirect('store_home')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, f"'{product.name}' has been listed successfully!")
            return redirect('seller_dashboard')
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form, 'title': 'List an Accessory'})


@login_required
def edit_accessory(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{product.name}' updated successfully.")
            return redirect('seller_dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'store/add_product.html', {'form': form, 'title': 'Edit Accessory', 'product': product})
