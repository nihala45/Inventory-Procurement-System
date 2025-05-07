from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    
    

    def __str__(self):
        return self.name

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class FinanceUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # Link to department if needed
    is_approver = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username} (Finance)"
    
# class PurchaseOrder(models.Model):
#     procurement_request = models.OneToOneField(ProcurementRequest, on_delete=models.CASCADE)
#     po_number = models.CharField(max_length=100, unique=True)
#     generated_date = models.DateField(default=timezone.now)
#     vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     pdf_file = models.FileField(upload_to='purchase_orders/', null=True, blank=True)
#     approval_date = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"PO {self.po_number} - Vendor: {self.vendor.name}"

#     def save(self, *args, **kwargs):
        
#         if not self.po_number:
#             last_po = PurchaseOrder.objects.order_by('-id').first()
#             next_po_number = f"PO-{timezone.now().year}-{(last_po.id + 1 if last_po else 1):03d}"
#             self.po_number = next_po_number
#         super().save(*args, **kwargs)
    
class ITEquipmentDetails(models.Model):
    name = models.CharField(max_length=100)
    warranty_period = models.CharField(max_length=50) 
    technical_specifications = models.TextField()
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    

class OfficeSupplyDetails(models.Model):
    name = models.CharField(max_length=100)
    preferred_brand = models.CharField(max_length=100)
    cost_per_item = models.DecimalField(max_digits=10, decimal_places=2)
    
    

CATEGORY_CHOICES = [
    ('IT Equipment', 'IT Equipment'),
    ('Office Supplies', 'Office Supplies'),
]

STATUS_CHOICES = [
    ('Pending Department Approval', 'Pending Department Approval'),
    ('Rejected by Department', 'Rejected by Department'),
    ('Pending Finance Approval', 'Pending Finance Approval'),
    ('Approved by Finance', 'Approved by Finance'),
    ('Rejected by Finance', 'Rejected by Finance'),
    ('PO Generated', 'PO Generated'),
    ('Fulfilled', 'Fulfilled'),
]

class ProcurementRequest(models.Model):
    requester = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    it_equipment = models.ForeignKey(ITEquipmentDetails, on_delete=models.SET_NULL, null=True, blank=True)
    office_supply = models.ForeignKey(OfficeSupplyDetails, on_delete=models.SET_NULL, null=True, blank=True)
    
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Department Approval')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.category == 'IT Equipment' and self.it_equipment:
            self.total_cost = int(self.quantity) * self.it_equipment.cost_per_item
        elif self.category == 'Office Supplies' and self.office_supply:
            self.total_cost = int(self.quantity) * self.office_supply.cost_per_item
        else:
            self.total_cost = 0
        super().save(*args, **kwargs)

    def __str__(self):
        # requester is already a string, so just use it directly:
        return f"{self.requester} - {self.category} - {self.status}"

    def get_equipment_name(self):
        if self.category == 'IT Equipment' and self.it_equipment:
            return self.it_equipment.name
        elif self.category == 'Office Supplies' and self.office_supply:
            return self.office_supply.name
        return "No Equipment"