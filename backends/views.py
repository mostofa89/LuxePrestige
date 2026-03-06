from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, IntegerField, When
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.db import transaction
import json
from .permissions import checkUserPermissions
from .models import Brand, Product, ProductCategory, ProductImage, UserPermission, Category, Inventory, Review, Membership, Customer, Cart, CartItem
from django.contrib.auth.models import User
from .utls import generate_otp, verify_otp, send_verification_confirmation_email
# Create your views here.

def dashboard(request):
    return render(request, 'backends/dashboard.html')


def paginate_list(page_number, data_list):
    items_per_page, max_pages = 10, 10
    paginator = Paginator(data_list, items_per_page)
    page_obj = paginator.get_page(page_number)
    try:
        data_list = paginator.page(page_number or 1)

    except PageNotAnInteger:
        data_list = paginator.page(1)

    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    current_page = data_list.number
    start_page = max(current_page - max_pages // 2, 1)
    end_page = start_page + max_pages
    if end_page > paginator.num_pages:
        end_page = paginator.num_pages
        start_page = max(end_page - max_pages, 1)

    paginator_list = range(start_page, end_page + 1)
    return page_obj, paginator_list





def brand(request):
    context = {}
    is_add_page = request.path.endswith('add_brand/')

    if request.method == 'POST':
        if not checkUserPermissions(request, 'can_add', '/backends/brand-list/'):
            return render(request, 'backends/403.html', status=403)
        name = request.POST.get('name')
        if name:
            if Brand.objects.filter(name__iexact=name).exists():
                context['error'] = 'Brand with this name already exists.'
                return render(request, 'backends/add_brand.html', context)
            
            else:
                Brand.objects.create(name=name)
                messages.success(request, 'Brand added successfully.')
                return redirect(request.path)
        context['error'] = 'Brand name is required.'

    if is_add_page:
        if not checkUserPermissions(request, 'can_add', '/backends/brand-list/'):
            return render(request, 'backends/403.html', status=403)
        return render(request, 'backends/add_brand.html', context)
    
    if request.method == 'GET':
        if not is_add_page:
            if not checkUserPermissions(request, 'can_view', '/backends/brand-list/'):
                return render(request, 'backends/403.html', status=403)
            
        brands = Brand.objects.all().order_by('name')
        page_number = request.GET.get('page')
        page_obj, paginator_list = paginate_list(page_number, brands)
        context.update({
            'brands': page_obj.object_list,
            'page_obj': page_obj,
            'paginator_list': paginator_list,
        })

        return render(request, 'backends/brand.html', context)
    

def category(request):
    context = {}
    is_add_page = request.path.endswith('add_category/')

    if request.method == 'POST':
        if not checkUserPermissions(request, 'can_add', '/backends/category-list/'):
            return render(request, 'backends/403.html', status=403)
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        category_image = request.FILES.get('category_image')
        is_active = request.POST.get('is_active') == 'on'
        
        if name and slug :
            if Category.objects.filter(name__iexact=name).exists():
                context['error'] = 'Category with this name already exists.'
                return render(request, 'backends/add_category.html', context)
            
            else:
                Category.objects.create(
                    name=name, 
                    slug=slug,
                    category_image=category_image,
                    is_active=is_active
                )
                messages.success(request, 'Category added successfully.')
                return redirect(request.path)
                
        context['error'] = 'Category name, slug and description are required.'

    if is_add_page:
        if not checkUserPermissions(request, 'can_add', '/backends/category-list/'):
            return render(request, 'backends/403.html', status=403)
        return render(request, 'backends/add_category.html', context)
    
    if request.method == 'GET':
        if not is_add_page:
            if not checkUserPermissions(request, 'can_view', '/backends/category-list/'):
                return render(request, 'backends/403.html', status=403)
            
        categories = Category.objects.all().order_by('name')
        page_number = request.GET.get('page')
        page_obj, paginator_list = paginate_list(page_number, categories)
        context.update({
            'categories': page_obj.object_list,
            'page_obj': page_obj,
            'paginator_list': paginator_list,
        })

        return render(request, 'backends/category.html', context)
    

def product(request):
    context = {}
    is_add_page = request.path.endswith('add_product/')
    brands = Brand.objects.filter(is_active=True).order_by('name')
    categories = Category.objects.filter(is_active=True).order_by('name')
    context.update({
        'brands': brands,
        'categories': categories,
    })

    if request.method == 'POST':
        if not checkUserPermissions(request, 'can_add', '/backends/product-list/'):
            return render(request, 'backends/403.html', status=403)
        
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        weight = request.POST.get('weight')
        category = request.POST.get('category')
        delivery_day_min = request.POST.get('delivery_day_min')
        delivery_day_max = request.POST.get('delivery_day_max')
        avl_quantity = request.POST.get('avl_quantity')
        product_image = request.FILES.get('product_image')
        is_active = request.POST.get('is_active') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'

        if name and slug and description and price and brand and weight and category and delivery_day_min and delivery_day_max:
            if Product.objects.filter(name__iexact=name).exists():
                context['error'] = 'Product with this name already exists.'
                return render(request, 'backends/add_product.html', context)
            
            else:
                Product.objects.create(
                    name = name,
                    slug = slug,
                    description = description,
                    price = price,
                    brand_id = brand,
                    weight = weight,
                    category_id = category,
                    delivery_day_max = delivery_day_max,
                    delivery_day_min = delivery_day_min,
                    avl_quantity = avl_quantity,
                    product_image = product_image,
                    is_active = is_active,
                    is_featured = is_featured,
                )
                messages.success(request, 'Product added successfully.')
                return redirect(request.path)
                
        context['error'] = 'All product fields are required.'

    if is_add_page:
        if not checkUserPermissions(request, 'can_add', '/backends/product-list/'):
            return render(request, 'backends/403.html', status=403)
        return render(request, 'backends/add_product.html', context)
    
    if request.method == 'GET':
        if not is_add_page:
            if not checkUserPermissions(request, 'can_view', '/backends/product-list/'):
                return render(request, 'backends/403.html', status=403)
            
        products = Product.objects.all().order_by('name')
        page_number = request.GET.get('page')
        page_obj, paginator_list = paginate_list(page_number, products)
        context.update({
            'products': page_obj.object_list,
            'page_obj': page_obj,
            'paginator_list': paginator_list,
        })

        return render(request, 'backends/product.html', context)


def product_details(request, product_id):
    product = Product.objects.select_related('brand', 'category').filter(id=product_id).first()
    product_images = ProductImage.objects.filter(product_id=product_id).order_by('position')
    if not product:
        return render(request, 'backends/404.html', status=404)
    
    context = {
        'product': product,
        'product_images': product_images,
    }
    return render(request, 'backends/product_details.html', context)


def add_product_category(request):
    context = {}
    is_add_page = request.path.endswith('add_product_category/')
    products = Product.objects.filter(is_active=True).order_by('name')
    categories = Category.objects.filter(is_active=True).order_by('name')
    context.update({
        'products': products,
        'categories': categories,
    })

    if request.method == 'POST':
        product = request.POST.get('product')
        category = request.POST.get('category')
        if product and category:
            if ProductCategory.objects.filter(product_id=product, category_id=category).exists():
                context['error'] = 'This product is already assigned to the selected category.'
                return render(request, 'backends/add_product_category.html', context)
            
            else:
                ProductCategory.objects.create(product_id=product, category_id=category)
                messages.success(request, 'Product category added successfully.')
                return redirect(request.path)
        
        context['error'] = 'Product and category are required.'
        return render(request, 'backends/add_product_category.html', context)
        

    elif is_add_page:
        return render(request, 'backends/add_product_category.html', context)
    

def product_category(request):
    context = {}
    if request.method == 'GET':      
        product_categories = ProductCategory.objects.select_related('product', 'category').order_by('product__name', 'category__name')
        page_number = request.GET.get('page')
        page_obj, paginator_list = paginate_list(page_number, product_categories)
        context.update({
            'product_categories': page_obj.object_list,
            'page_obj': page_obj,
            'paginator_list': paginator_list,
        })

        return render(request, 'backends/productlist.html', context)
    
def add_product_image(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        image = request.FILES.get('image')
        position = request.POST.get('position', 0)
        alt_text = request.POST.get('alt_text', '')
        if product and image:
            product = Product.objects.filter(id=product, is_active=True).first()
            if product:
                ProductImage.objects.create(product=product, image=image, position=position, alt_text=alt_text)
                messages.success(request, 'Product image added successfully.')
                return redirect('backends:add_product_image')
        
        messages.error(request, 'Product and image are required.')
        return redirect('backends:add_product_image')
    
    context = {
        'products': Product.objects.filter(is_active=True).order_by('name'),
    }
    return render(request, 'backends/add_product_image.html', context)
    

def product_image_list(request):
    product_images = ProductImage.objects.select_related('product').order_by('product__name', 'position')
    page_number = request.GET.get('page')
    page_obj, paginator_list = paginate_list(page_number, product_images)
    context = {
            'product_images': page_obj.object_list,
            'page_obj': page_obj,
            'paginator_list': paginator_list,
    }

    return render(request, 'backends/product_images.html', context)


def inventory_list(request):
    inventory_list = Inventory.objects.select_related('product').order_by('product__name')
    page_number = request.GET.get('page')
    page_obj, paginator_list = paginate_list(page_number, inventory_list)
    context = {
            'inventory_list': page_obj.object_list,
            'page_obj': page_obj,
            'paginator_list': paginator_list,
    }

    return render(request, 'backends/inventory.html', context)
    
    
def inventory_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        restock_date = request.POST.get('restock_date')
        
        if product_id and quantity and restock_date:
            inventory, created = Inventory.objects.get_or_create(
                product_id=product_id,
                stock_quantity=quantity,
                restock_date=restock_date,
            )

            if restock_date:
                inventory.restock_date = restock_date
            inventory.save()
            messages.success(request, 'Inventory updated successfully.')
            return redirect('backends:inventory')
        
        messages.error(request, 'Product, quantity, and restock date are required.')
        return redirect('backends:inventory_add')
    
    products = Product.objects.filter(is_active=True).order_by('name')
    return render(request, 'backends/add_to_inventory.html', {'products': products})


def get_products_json(request):
    """Return products as JSON for dynamic dropdown updates"""
    products = Product.objects.filter(is_active=True).order_by('name').values('id', 'name')
    return JsonResponse(list(products), safe=False)


def get_categories_json(request):
    """Return categories as JSON for dynamic dropdown updates"""
    categories = Category.objects.filter(is_active=True).order_by('name').values('id', 'name')
    return JsonResponse(list(categories), safe=False)


def membership_list(request):
    """Display all memberships with pagination"""
    memberships = Membership.objects.annotate(
        tier_order=Case(
            When(tier='bronze', then=0),
            When(tier='silver', then=1),
            When(tier='gold', then=2),
            When(tier='platinum', then=3),
            When(tier='diamond', then=4),
            default=99,
            output_field=IntegerField(),
        )
    ).order_by('tier_order', 'id')

    tier_policy = {
        'bronze': {'range': '0-9,999', 'discount': '0%'},
        'silver': {'range': '10,000-19,999', 'discount': '3%'},
        'gold': {'range': '20,000-29,999', 'discount': '7%'},
        'platinum': {'range': '30,000-39,999', 'discount': '11%'},
        'diamond': {'range': '40,000+', 'discount': '15%'},
    }
    
    # Parse benefits for each membership
    for membership in memberships:
        membership.benefits = [b.strip() for b in membership.benefits.split('\n') if b.strip()]
    
    page_number = request.GET.get('page')
    page_obj, paginator_list = paginate_list(page_number, memberships)
    
    context = {
        'memberships': page_obj,
        'page_obj': page_obj,
        'paginator_list': paginator_list,
        'paginator': Paginator(memberships, 10),
        'tier_policy': tier_policy,
    }
    return render(request, 'backends/memberships.html', context)


def add_membership(request):
    """Add or edit a membership"""
    context = {}
    membership = None
    membership_id = request.GET.get('id')
    
    if membership_id:
        try:
            membership = Membership.objects.get(id=membership_id)
            if membership.benefits:
                membership.benefits = [b.strip() for b in membership.benefits.split('\n') if b.strip()]
            context['membership'] = membership
        except Membership.DoesNotExist:
            context['error'] = 'Membership not found.'
            return render(request, 'backends/add_membership.html', context)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        tier = request.POST.get('tier')
        description = request.POST.get('description')
        benefits_text = request.POST.get('benefits')
        is_active = request.POST.get('is_active') == 'on'
        is_featured = request.POST.get('is_featured') == 'on'
        
        if not name or not tier:
            context['error'] = 'Name and Tier are required.'
            if membership:
                context['membership'] = membership
            return render(request, 'backends/add_membership.html', context)
        
        if membership:
            # Update existing membership
            membership.name = name
            membership.tier = tier
            membership.description = description
            membership.benefits = benefits_text
            membership.is_active = is_active
            membership.is_featured = is_featured
            membership.save()
            messages.success(request, 'Membership updated successfully.')
        else:
            # Create new membership
            membership = Membership(
                name=name,
                tier=tier,
                description=description,
                benefits=benefits_text,
                is_active=is_active,
                is_featured=is_featured
            )
            membership.save()
            messages.success(request, 'Membership created successfully.')
        
        return redirect('backends:memberships')
    
    context['membership'] = membership
    return render(request, 'backends/add_membership.html', context)


def Login(request):

    if request.method == 'POST':
        username_input = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # Find user by email or username
        user_obj = None
        if '@' in username_input:
            user_obj = User.objects.filter(email__iexact=username_input).first()
        else:
            user_obj = User.objects.filter(username__iexact=username_input).first()

        # Check if user exists
        if not user_obj:
            messages.error(request, 'Invalid email, username, or password.')
            return render(request, 'backends/login.html')

        # Check if user account is active
        if not user_obj.is_active:
            messages.error(request, 'Your account is not activated. Please verify your email first.')
            return render(request, 'backends/login.html')

        # Authenticate user
        user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('backends:dashboard')

        messages.error(request, 'Invalid email, username, or password.')
        return render(request, 'backends/login.html')

    return render(request, 'backends/login.html')


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password1 = request.POST.get('password1', '').strip()
        password2 = request.POST.get('confirm_password', '').strip()
        dob = request.POST.get('dob', '').strip()

        # Validate required fields
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'backends/register.html')
        
        if not email:
            messages.error(request, 'Email is required.')
            return render(request, 'backends/register.html')
        
        if not phone:
            messages.error(request, 'Phone number is required.')
            return render(request, 'backends/register.html')
        
        if not password1 or not password2:
            messages.error(request, 'Both password fields are required.')
            return render(request, 'backends/register.html')

        # Validate email format
        user = None
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email format.')
            return render(request, 'backends/register.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'backends/register.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists() or Customer.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'backends/register.html')

        # Validate passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'backends/register.html')
        
        # Validate password length
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'backends/register.html')

        try:
            # Create Django User
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password1
            )
            user.is_active = True
            user.save()
            
            # Create Customer profile with phone and dob
            Customer.objects.create(
                customer=user,
                name=username,
                email=email,
                password=password1,  # Note: storing plain password is not recommended
                phone=phone,
                dob=dob,
                is_active=True
            )
            
            # Generate and send OTP for verification
            generate_otp(email, username=username)
            
            messages.success(request, 'Registration successful! Please verify your email with the OTP sent.')
            return redirect('backends:verify_otp', user_id=user.id)
        
        except Exception as e:
            # Rollback if Customer creation fails
            if user:
                user.delete()
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'backends/register.html')

    return render(request, 'backends/register.html')


def VerifyOTP(request, user_id):
    """Verify OTP sent to user's email during registration"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('backends:register')
    
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        
        if not otp:
            messages.error(request, 'Please enter the OTP.')
            return render(request, 'backends/verify_otp.html', {'user': user})
        
        # Verify OTP using the utility function
        is_valid, message = verify_otp(user.email, otp)
        
        if is_valid:
            # Activate the user account
            user.is_active = True
            user.save()
            
            # Also mark the Customer record as active
            try:
                customer = Customer.objects.get(customer=user)
                customer.is_active = True
                customer.save()
            except Customer.DoesNotExist:
                pass

            send_verification_confirmation_email(user.email, username=user.username)
            
            messages.success(request, 'Email verified successfully! You can now login.')
            return redirect('backends:login')
        else:
            messages.error(request, message)
            return render(request, 'backends/verify_otp.html', {'user': user})
    
    # GET request - show OTP form
    context = {
        'user': user,
        'email': user.email,
    }
    return render(request, 'backends/verify_otp.html', context)


def ResendOTP(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('backends:register')

    otp = generate_otp(user.email, username=user.username)
    if otp:
        messages.success(request, 'A new verification code has been sent to your email.')
    else:
        messages.error(request, 'Failed to send a new verification code. Please try again.')

    return redirect('backends:verify_otp', user_id=user.id)


def Logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('backends:login')


def cart_ammount_summary(request):
    sub_total = 0
    total_val = 0
    total_discount = 0
    grand_total = 0

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(customer=request.user)
            cart = Cart.objects.filter(customer=customer).first()
            if cart:
                cart_items = CartItem.objects.filter(cart=cart).select_related('product')
                for item in cart_items:
                    sub_total += float(item.product.price) * item.quantity
        except Customer.DoesNotExist:
            pass

    grand_total = (sub_total + total_val) - total_discount
    return {
        'sub_total': float(sub_total),
        'tax_amount': float(total_val),
        'total_discount': float(total_discount),
        'grand_total': float(grand_total)
    }


def add_to_cart(request):
    if not request.user.is_authenticated:
        return JsonResponse({
            'status': 'error',
            'message': 'User is not authenticated. Please log in to add products to cart.'
        }, status=401)

    if request.method == 'POST':
        try:
            # Get customer
            customer = Customer.objects.filter(customer=request.user).first()
            if not customer:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Customer profile not found.'
                }, status=404)

            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('quantity', 1))

            # Validate inputs
            if not product_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Product ID is required.'
                }, status=400)

            if quantity < 1:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Quantity must be at least 1.'
                }, status=400)

            # Get product
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Product not found.'
                }, status=404)

            # Check product availability
            if not product.is_active:
                return JsonResponse({
                    'status': 'error',
                    'message': 'This product is currently unavailable.'
                }, status=400)

            # Get or create cart
            cart, cart_created = Cart.objects.get_or_create(customer=customer)

            # Get or create cart item
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )

            if not item_created:
                # Update quantity
                cart_item.quantity += quantity
                
                # Check stock availability
                if cart_item.quantity > product.avl_quantity:
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Cannot add {quantity} more. Only {product.avl_quantity} items available in stock.'
                    }, status=400)
                
                cart_item.save()

            # Get cart summary
            ammount_summary = cart_ammount_summary(request)
            cart_item_count = CartItem.objects.filter(cart=cart).count()
            total_items = sum(item.quantity for item in CartItem.objects.filter(cart=cart))

            response = {
                'status': 'success',
                'message': f'{product.name} has been added to your cart.',
                'cart_item_count': cart_item_count,
                'total_items': total_items,
                'ammount_summary': ammount_summary,
                'item_price': float(product.price),
                'product_name': product.name,
                'quantity': cart_item.quantity
            }

            return JsonResponse(response)
        
        except ValueError as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid quantity value: {str(e)}'
            }, status=400)
        
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Failed to add product to cart: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)


def cartItem(request):
    """
    View to handle cart item operations:
    - GET: Display all cart items
    - POST: Update or delete cart items
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to view your cart.')
        return redirect('backends:login')

    try:
        customer = Customer.objects.get(customer=request.user)
    except Customer.DoesNotExist:
        messages.error(request, 'Customer profile not found.')
        return redirect('backends:login')

    # Get or create cart
    cart, created = Cart.objects.get_or_create(customer=customer)

    # Handle POST request - Update or Delete cart items
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item_id = request.POST.get('cart_item_id')

        if not action or not cart_item_id:
            messages.error(request, 'Invalid request.')
            return redirect('backends:cart_items')

        # Get cart item
        try:
            cart_item = CartItem.objects.select_related('product').get(
                id=cart_item_id,
                cart=cart
            )
        except CartItem.DoesNotExist:
            messages.error(request, 'Cart item not found.')
            return redirect('backends:cart_items')

        # Handle UPDATE action
        if action == 'update':
            quantity = request.POST.get('quantity')
            
            if not quantity:
                messages.error(request, 'Quantity is required.')
                return redirect('backends:cart_items')

            try:
                quantity = int(quantity)
            except ValueError:
                messages.error(request, 'Invalid quantity value.')
                return redirect('backends:cart_items')

            if quantity < 1:
                messages.error(request, 'Quantity must be at least 1.')
                return redirect('backends:cart_items')

            # Check stock availability
            if quantity > cart_item.product.avl_quantity:
                messages.error(request, f'Only {cart_item.product.avl_quantity} items available in stock.')
                return redirect('backends:cart_items')

            # Update quantity
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart item updated successfully.')
            return redirect('backends:cart_items')

        # Handle DELETE action
        elif action == 'delete':
            product_name = cart_item.product.name
            cart_item.delete()
            messages.success(request, f'{product_name} has been removed from your cart.')
            return redirect('backends:cart_items')

        else:
            messages.error(request, 'Invalid action.')
            return redirect('backends:cart_items')

    # Handle GET request - Display cart items
    cart_items = CartItem.objects.filter(cart=cart).select_related(
        'product', 
        'product__brand', 
        'product__category'
    )
    
    # Add subtotal to each item
    items_with_subtotal = []
    for item in cart_items:
        item.subtotal = float(item.product.price) * item.quantity
        items_with_subtotal.append(item)
    
    # Calculate totals
    sub_total = sum(item.subtotal for item in items_with_subtotal)
    
    # Get customer discount from membership
    discount_percentage = 0
    if customer.membership:
        discount_percentage = float(customer.membership.discount_percentage)
    elif customer.points_discount_percentage:
        discount_percentage = float(customer.points_discount_percentage)
    
    discount_amount = (sub_total * discount_percentage) / 100
    tax_amount = (sub_total - discount_amount) * 0.1  # 10% tax
    grand_total = sub_total - discount_amount + tax_amount
    
    cart_item_count = len(items_with_subtotal)
    total_items = sum(item.quantity for item in items_with_subtotal)

    context = {
        'cart_items': items_with_subtotal,
        'cart_item_count': cart_item_count,
        'total_items': total_items,
        'sub_total': sub_total,
        'discount_percentage': discount_percentage,
        'discount_amount': discount_amount,
        'tax_amount': tax_amount,
        'grand_total': grand_total,
        'customer': customer,
    }

    return render(request, 'backends/cart_items.html', context)
                  

                    
