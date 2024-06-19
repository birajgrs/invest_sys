# models.py
from django.db import models

class BankTransaction(models.Model):
    future_date = models.DateField()
    bank_name = models.CharField(max_length=100, default="Default Bank")
    deposit_type = models.CharField(max_length=100, default="Default Deposit Type")
    amount = models.IntegerField()
    total_interest = models.IntegerField(default=0)
    total_amount =models.IntegerField(default=0)
    days  =models.IntegerField(default=0)

    def __str__(self):
        return f"{self.future_date} - {self.bank_name} - {self.deposit_type} - {self.amount} - {self.total_interest} - {self.total_amount}"


class BankInterest(models.Model):
    bank_name = models.CharField(max_length=100)
    deposit_type = models.CharField(max_length=20)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    from_date = models.DateField()

    def __str__(self):
        return f"{self.bank_name} - {self.deposit_type} - {self.interest_rate}% - {self.from_date}"



