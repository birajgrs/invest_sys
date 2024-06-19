from django.contrib import admin

# Register your models here.
from .models import SelfBankInvestment
admin.site.register(SelfBankInvestment)

from .models import BusinessHouseData
admin.site.register(BusinessHouseData)

from .models import FinancialData
admin.site.register(FinancialData)