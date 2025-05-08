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
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  
    is_approver = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username} (Finance)"
    

    
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

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.category == 'IT Equipment' and self.it_equipment:
            self.total_cost = int(self.quantity) * self.it_equipment.cost_per_item
        elif self.category == 'Office Supplies' and self.office_supply:
            self.total_cost = int(self.quantity) * self.office_supply.cost_per_item
        else:
            self.total_cost = 0
        print(f"Total Cost: {self.total_cost}")
        super().save(*args, **kwargs)

    def __str__(self):
        
        return f"{self.requester} - {self.category} - {self.status}"

    def get_equipment_name(self):
        if self.category == 'IT Equipment' and self.it_equipment:
            return self.it_equipment.name
        elif self.category == 'Office Supplies' and self.office_supply:
            return self.office_supply.name
        return "No Equipment"
    
    
class PurchaseOrder(models.Model):
    request = models.ForeignKey(ProcurementRequest, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2) 
    issued_at = models.DateTimeField(auto_now_add=True)
    fulfilled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO Number: {self.po_number}"
    

