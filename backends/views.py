from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Brand
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
        return render(request, 'backends/add_brand.html', context)
    
    if request.method == 'GET':
        brands = Brand.objects.all().order_by('name')
        page_number = request.GET.get('page')
        page_obj, paginator_list = paginate_list(page_number, brands)
        context.update({
            'brands': page_obj.object_list,
            'page_obj': page_obj,
            'paginator_list': paginator_list,
        })

        return render(request, 'backends/brand.html', context)
    




