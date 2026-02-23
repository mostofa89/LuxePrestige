from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Case, IntegerField, When
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .permissions import checkUserPermissions
from .models import Brand, Product, ProductCategory, ProductImage, UserPermission, Category, Inventory, Review, Membership
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
    return render(request, 'backends/login.html')
    




