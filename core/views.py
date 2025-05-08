from django.shortcuts import render, redirect, get_object_or_404
from .models import ITEquipmentDetails, OfficeSupplyDetails, Department, ProcurementRequest, PurchaseOrder
from django.http import JsonResponse
from django.http import Http404

from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import PurchaseOrder


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
        print(requester_name, 'Hellooohhhhhhhhhhhhhhhhh')
        
        department_id = request.POST.get('department')
        print(department_id,'this the department')
        category = request.POST.get('category')
        print(category,'category management simple',)
        quantity = request.POST.get('quantity')
        print(quantity,'quantity management simple',)
        
        description = request.POST.get('description')
        print(description,'description management')
        
        equipment_id = request.POST.get('equipment')
        print(equipment_id,'this is the equiment id u got')

        
        department = Department.objects.get(id=department_id)
        
        if category == 'IT Equipment':
            equipment = ITEquipmentDetails.objects.get(id=equipment_id)
            print(equipment,'iiiiiiiiiiiiiiiiit equitmemt')
        elif category == 'Office Supply':
            equipment = OfficeSupplyDetails.objects.get(id=equipment_id)
            print(equipment,'ooooooooooyou got this equipemnt')
        else:
            equipment = None

       
        if equipment:
            if category == 'IT Equipment':
                total_cost = int(quantity) * equipment.cost_per_item
                print(total_cost,'iiiiiiiiiiiii')
            elif category == 'Office Supply':
                total_cost = int(quantity) * equipment.cost_per_item
                print(total_cost,'Ooooooooooooooooooo')
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

        return redirect('home')

    return render(request, 'create_procurement.html')

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
        if procurement_request.department.budget > procurement_request.total_cost:
            new_status = request.POST.get('status')
            if new_status:
                procurement_request.status = new_status
                procurement_request.save()
                return JsonResponse({'success': True, 'message': 'Status updated successfully'})
    
    return JsonResponse({'success': False, 'message': 'Failed to update status'})




def finance_dashboard(request):
    
    procurement_requests = ProcurementRequest.objects.filter(
        status__in=[
            'Pending Finance Approval',
            'Approved by Finance',
            'Rejected by Finance'
        ]
    )
    print(procurement_requests, 'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
    return render(request, 'finance_dashboard.html', {
        'requests': procurement_requests
    })



    return JsonResponse({'success': True, 'message': 'Status updated successfully'})
    
    return JsonResponse({'success': False, 'message': 'Failed to update status'})









def approve_request(request, request_id):  
    print('sssssssssssssssssssssssssss')
    procurement_request = get_object_or_404(ProcurementRequest, id=request_id)

    
    print('heeeeeeeeeeeeeeeeeeeeeeeeeellllllllllllll')
    procurement_request.status = 'Approved by Finance'
    procurement_request.save()

        
    context = {
        'request': procurement_request,
        'total_cost': procurement_request.total_cost,
    }
    html = render_to_string('pdf_template.html', context)

        
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PO_{procurement_request.id}.pdf"'

        
    pisa_status = pisa.CreatePDF(html, dest=response)

        
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)

    return response  

    
    

def reject_request(request):
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        reason = request.POST.get('rejection_reason')
        req = get_object_or_404(ProcurementRequest, id=req_id)
        req.status = 'Rejected by Finance'
        
        req.save()
    return redirect('finance_dashboard')

