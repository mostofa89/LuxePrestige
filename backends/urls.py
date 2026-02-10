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
    path('login/', views.Login, name='login')
]
