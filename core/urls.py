from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('get-products/', views.get_products, name='get_products'),
]
