from django.db import models
from datetime import date
from decimal import Decimal
from django.utils import timezone

class BusinessHouseData(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    founded_date = models.DateField()
    location = models.CharField(max_length=200)
    website = models.URLField()
    type_of_service_or_product = models.CharField(max_length=200)
    total_investment = models.IntegerField()
    initial_investment = models.IntegerField()
    discount_rate = models.FloatField()
    operational_days = models.IntegerField()
    project_lifetime = models.IntegerField()

    def __str__(self):
        return self.name

class BusinessHouseRelationship(models.Model):
    from_business_house = models.ForeignKey(BusinessHouseData, related_name='from_businesses', on_delete=models.CASCADE)
    to_business_house = models.ForeignKey(BusinessHouseData, related_name='to_businesses', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=100)  # You can use this field to define the type of relationship, like "NEA to Railway"

    def __str__(self):
        return f"{self.from_business_house.name} to {self.to_business_house.name} ({self.relationship_type})"



from django.db import models
from django.utils import timezone

class FinancialData(models.Model):
    business_house = models.ForeignKey(BusinessHouseData, on_delete=models.CASCADE, related_name='financial_data', null=True, blank=True)
    transaction_date = models.DateField(default=timezone.now)
    daily_income = models.FloatField()
    daily_expenses_extra = models.FloatField()
    business_house_relation = models.ForeignKey(BusinessHouseRelationship, on_delete=models.CASCADE, related_name='financial_data', null=True, blank=True)


    def save(self, *args, **kwargs):
        # Check if there is an existing record with the same data
        existing_data = FinancialData.objects.filter(
            transaction_date = self.transaction_date,
            business_house=self.business_house,
            daily_income=self.daily_income,
            daily_expenses_extra=self.daily_expenses_extra,
        ).first()

        # If an existing record is found, delete it
        if existing_data:
            existing_data.delete()

        # Save the current instance
        super().save(*args, **kwargs)

















class SelfBankInvestment(models.Model):
    name = models.CharField(max_length=100, default='Default Name')
    invest_amount = models.IntegerField(default=0)
    bank_name = models.CharField(max_length=100, default=None)
    loan_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    ROI_Date = models.DateField()
    interest = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_date = models.DateField(default=date.today)

    def calculate_interest(self):
        invest_amount = Decimal(self.invest_amount)
        loan_rate = self.loan_rate / Decimal(100)
        years = Decimal((self.ROI_Date - self.created_date).days) / Decimal(365)
        return invest_amount * loan_rate * years

    def save(self, *args, **kwargs):
        self.interest = self.calculate_interest()
        self.total_amount = self.invest_amount + self.interest
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Investment amount: {self.invest_amount}, Bank: {self.bank_name}, Future Date: {self.ROI_Date}"
