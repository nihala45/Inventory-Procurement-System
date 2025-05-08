from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('get-products/', views.get_products, name='get_products'),
    path('create_procurement/', views.create_procurement, name='create_procurement'),
    path('view_departments/', views.view_departments, name='view_departments'),
    path('department_details/<int:dep_id>/', views.department_details, name='department_details'),
    path('update-status/<int:request_id>/', views.update_status, name='update_status'),
    path('finance_dashboard/', views.finance_dashboard, name='finance_dashboard'),
   
    path('approve_request/<int:request_id>/', views.approve_request, name='approve_request'),


    path('reject_request/<int:request_id>/', views.reject_request, name='reject_request'),
    path('vendor_view/', views.vendor_view, name='vendor_view'),
    path('vendor/<int:v_id>/customers/', views.customer_details, name='customer_details'),
    path('update_request_status/<int:r_id>/', views.update_request_status, name='update_request_status'),
    
]
