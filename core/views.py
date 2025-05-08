from django.shortcuts import render, redirect, get_object_or_404
from .models import ITEquipmentDetails, OfficeSupplyDetails, Department, ProcurementRequest, PurchaseOrder, Vendor
from django.http import JsonResponse
from django.http import Http404

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import PurchaseOrder
from django.utils import timezone
from django.contrib import messages


def home(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'form.html', context)
    
    

def get_products(request):
    category = request.GET.get('category')
    products = []

    if category == "IT Equipment":
        products = list(ITEquipmentDetails.objects.all().values('id', 'name'))
    elif category == "Office Supply":
        products = list(OfficeSupplyDetails.objects.all().values('id', 'name'))
    return JsonResponse({'products': products})




def create_procurement(request):
    if request.method == 'POST':
        requester_name = request.POST.get('requester_name')
        department_id = request.POST.get('department')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        equipment_id = request.POST.get('equipment')
        
        department = Department.objects.get(id=department_id)

        if category == 'IT Equipment':
            equipment = ITEquipmentDetails.objects.get(id=equipment_id)
        elif category == 'Office Supply':
            equipment = OfficeSupplyDetails.objects.get(id=equipment_id)
        else:
            equipment = None

        if equipment:
            if category == 'IT Equipment':
                total_cost = int(quantity) * equipment.cost_per_item
            elif category == 'Office Supply':
                total_cost = int(quantity) * equipment.cost_per_item
        else:
            total_cost = 0

        procurement_request = ProcurementRequest(
            requester=requester_name,
            department=department,
            category=category,
            quantity=quantity,
            total_cost=total_cost,
            description=description,
        )

        if category == 'IT Equipment':
            procurement_request.it_equipment = equipment
        elif category == 'Office Supply':
            procurement_request.office_supply = equipment

        procurement_request.save()

        # Add a success message
        messages.success(request, 'Procurement request has been successfully created.')

        return redirect('home')

    



def view_departments(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'departments.html', context)

def department_details(request, dep_id):
    department = Department.objects.filter(id = dep_id).first()
    if not department:
        raise Http404('Department not found')
    
    ProcurementRequest_request = ProcurementRequest.objects.filter(department=department)
    print(ProcurementRequest_request,'ssssssssssssssssssssssssss')
    context = {
        'department': department,
        'procurement_requests': ProcurementRequest_request
    }

    return render(request, 'department_details.html', context)


def update_status(request, request_id):
    procurement_request = get_object_or_404(ProcurementRequest, id=request_id)

    if request.method == 'POST':
        # Debugging: Print budget and total cost to ensure the condition is correct
        print(f"Budget: {procurement_request.department.budget}, Total Cost: {procurement_request.total_cost}")

        # Check if the department's budget is greater than the procurement request's total cost
        if procurement_request.department.budget > procurement_request.total_cost:
            new_status = request.POST.get('status')
            if new_status:
                procurement_request.status = new_status
                procurement_request.save()
                return JsonResponse({'success': True, 'message': 'Status updated successfully'})
        else:
            # Handle the case where the budget is not enough
            return JsonResponse({'success': False, 'message': 'Insufficient budget to approve the request'})

    return JsonResponse({'success': False, 'message': 'Failed to update status'})


def finance_dashboard(request):
    vendors = Vendor.objects.all()
    
    procurement_requests = ProcurementRequest.objects.filter(
        status__in=[
            'Pending Finance Approval',
            'Approved by Finance',
            'Rejected by Finance'
        ]
    )
    print(procurement_requests, 'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    return render(request, 'finance_dashboard.html', {
        'requests': procurement_requests,
        'vendors': vendors
    })



    return JsonResponse({'success': True, 'message': 'Status updated successfully'})
    
    return JsonResponse({'success': False, 'message': 'Failed to update status'})











from .models import ProcurementRequest, Vendor, PurchaseOrder
from django.utils import timezone
from django.http import HttpResponse
from xhtml2pdf import pisa

def approve_request(request, request_id):
    procurement_request = get_object_or_404(ProcurementRequest, id=request_id)

    
    if request.method == 'POST':
        vendor_id = request.POST.get('vendor_id')
        vendor = get_object_or_404(Vendor, id=vendor_id)
        print(vendor,'this ist he code details')

        procurement_request.status = 'Approved by Finance'
         
        procurement_request.save()

        po_number = f"PO-{procurement_request.id}-{vendor.id}"
        total_cost = procurement_request.total_cost

        
        purchase_order = PurchaseOrder.objects.create(
            request=procurement_request,
            vendor=vendor,
            po_number=po_number,
            total_cost=total_cost,
            issued_at=timezone.now(),
            fulfilled_at=None
        )

        
        context = {
            'request': procurement_request,
            'purchase_order': purchase_order,
            'vendor': vendor,
            'total_cost': total_cost,
        }

        
        html = render_to_string('pdf_template.html', context)

       
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="PO_{purchase_order.po_number}.pdf"'

        
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('Error generating PDF', status=500)

        return response

    
    vendors = Vendor.objects.all()
    context = {
        'request': procurement_request,
        'vendors': vendors,
    }
    return render(request, 'approve_request.html', context)


def reject_request(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        reason = request.POST.get('rejection_reason')
        req = get_object_or_404(ProcurementRequest, id=req_id)
        req.status = 'Rejected by Finance'
        
        req.save()
    return redirect('finance_dashboard')



def vendor_view(request):
    vendor = Vendor.objects.all()
    context = {
        'vendor': vendor
    }
    return render(request, 'vendor_view.html', context)

def customer_details(request, v_id):
    requester = ProcurementRequest.objects.filter(vendor_id=v_id)
    
    context = {
        'requesters': requester
    }
    
    return render(request, 'customer_details.html', context)


def update_request_status(request, r_id):
    if request.method == 'POST':
        purchase = get_object_or_404(ProcurementRequest, id=r_id)
        new_status = request.POST.get('status')

        if new_status in ['Fulfilled', 'Rejected']:
            purchase.status = new_status
            purchase.save()

    return redirect('finance_dashboard') 
    