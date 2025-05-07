from django.shortcuts import render
from .models import ITEquipmentDetails, OfficeSupplyDetails
from django.http import JsonResponse
# Create your views here.

def home(request):
    return render(request, 'form.html')

def get_products(request):
    category = request.GET.get('category')
    products = []

    if category == "IT Equipment":
        products = list(ITEquipmentDetails.objects.all().values('id', 'name'))
    elif category == "Office Supply":
        products = list(OfficeSupplyDetails.objects.all().values('id', 'name'))

    return JsonResponse({'products': products})