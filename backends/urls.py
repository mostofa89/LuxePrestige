from django.urls import path
from . import views

app_name = 'backends'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('brand/', views.brand, name='brand'),
    path('add_brand/', views.brand, name='add_brand'),
    path('login/', views.Login, name='login')
]
