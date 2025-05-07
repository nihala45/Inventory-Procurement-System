from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('get-products/', views.get_products, name='get_products'),
    path('create_procurement/', views.create_procurement, name='create_procurement'),
    path('view_departments/', views.view_departments, name='view_departments'),
    path('department_details/<int:dep_id>/', views.department_details, name='department_details'),
    path('update-status/<int:request_id>/', views.update_status, name='update_status'),
    
]
