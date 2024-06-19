from django.contrib import admin

# Register your models here.
from .models import BankTransaction
admin.site.register(BankTransaction)

from .models import BankInterest
admin.site.register(BankInterest)

