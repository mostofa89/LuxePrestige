from django.urls import path
from . import views

app_name = 'backends'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('brand/', views.brand, name='brand'),
    path('add_brand/', views.brand, name='add_brand'),
    path('category/', views.category, name='category'),
    path('add_category/', views.category, name='add_category'),
    path('product/', views.product, name='product'),
    path('add_product/', views.product, name='add_product'),
    path('add_product_category/', views.add_product_category, name='add_product_category'),
    path('product_category/', views.product_category, name='product_category'),
    path('add_product_image/', views.add_product_image, name='add_product_image'),
    path('product_images/', views.product_image_list, name='product_images'),
    path('inventory/', views.inventory_list, name='inventory'),
    path('add_inventory/', views.inventory_add, name='add_inventory'),
    path('api/products/', views.get_products_json, name='get-products-json'),
    path('api/categories/', views.get_categories_json, name='get-categories-json'),
    path('login/', views.Login, name='login')
]
