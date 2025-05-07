from django.db import models
from django.contrib.auth.models import User

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
    is_approver = models.BooleanField(default=False)  # Can approve requests

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
    ('Rejected by Finance', 'Rejected by Finance'),
    ('PO Generated', 'PO Generated'),
    ('Fulfilled', 'Fulfilled'),
]

class ProcurementRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    equipment = models.ForeignKey(ITEquipmentDetails, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending Department Approval')
    submitted_at = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.cost_per_item
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item_name} - {self.status}"

    