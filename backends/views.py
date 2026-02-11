from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.shortcuts import redirect, render
from .permissions import checkUserPermissions
from .models import Brand, Product, ProductCategory, UserPermission, Category, Inventory, Review
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
        if name and slug:
            if Category.objects.filter(name__iexact=name).exists():
                context['error'] = 'Category with this name already exists.'
                return render(request, 'backends/add_category.html', context)
            
            else:
                Category.objects.create(name=name, slug=slug)
                messages.success(request, 'Category added successfully.')
                return redirect(request.path)
                
        context['error'] = 'Category name and slug are required.'

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


def reviews(request):
    reviews = Review.objects.filter(is_active=True).select_related('product', 'user').order_by('-created_at')
    page_number = request.GET.get('page')
    page_obj, paginator_list = paginate_list(page_number, reviews)
    context = {
        'reviews': page_obj.object_list,
        'page_obj': page_obj,
        'paginator_list': paginator_list,
    }
    return render(request, 'backends/reviews.html', context)

def Login(request):
    return render(request, 'backends/login.html')
    




