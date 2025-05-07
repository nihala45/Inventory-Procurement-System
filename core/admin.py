from django.contrib import admin
from .models import Department, Vendor, ProcurementRequest, FinanceUser, ITEquipmentDetails, OfficeSupplyDetails
# Register your models here.
admin.site.register(Department)
admin.site.register(Vendor)
admin.site.register(ProcurementRequest)
admin.site.register(FinanceUser)
admin.site.register(ITEquipmentDetails)
admin.site.register(OfficeSupplyDetails)


