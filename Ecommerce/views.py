from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings
from backends.models import Product, Category, ProductImage
import os


def Home(request):
    categories = Category.objects.filter(is_active=True)
    category = categories.first()
    products = Product.objects.filter(is_active=True)[:12]
    product_images = ProductImage.objects.filter(is_active=True).order_by("position", "id")

    image_by_product_id = {}
    for image in product_images:
        if image.product_id not in image_by_product_id:
            image_by_product_id[image.product_id] = image

    product_cards = []
    for product in products:
        product_cards.append({
            "product": product,
            "image": image_by_product_id.get(product.id),
        })
    context = {
        'user': request.user,
        'is_authenticated': request.user.is_authenticated,
        'category': category,
        'categories': categories,
        'products': products,
        'product_images': product_images,
        'product_cards': product_cards,
    }
    return render(request, 'home/index.html', context)


def health_check(request):
    """Health check endpoint for debugging deployment"""
    return JsonResponse({
        'status': 'ok',
        'debug': settings.DEBUG,
        'environment': os.getenv('ENVIRONMENT', 'not set'),
        'allowed_hosts': settings.ALLOWED_HOSTS,
        'database': settings.DATABASES['default']['ENGINE'].split('.')[-1],
    })