from django import forms
from .models import SelfBankInvestment, BusinessHouseData

class SelfBankInvestmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SelfBankInvestmentForm, self).__init__(*args, **kwargs)
        self.fields['invest_amount'].required = True
        self.fields['bank_name'].required = False
        self.fields['loan_rate'].required = False
        self.fields['bank_name'].initial = 'Self Investment'
        self.fields['loan_rate'].initial = 0
        self.fields['ROI_Date'].widget = forms.DateInput(attrs={'type': 'date'})

    class Meta:
        model = SelfBankInvestment
        fields = ['invest_amount', 'bank_name', 'loan_rate', 'ROI_Date']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        return instance

class BusinessHouseForm(forms.ModelForm):
    class Meta:
        model = BusinessHouseData
        fields = '__all__' 

# forms.py
from django import forms
from .models import FinancialData

class FinancialDataForm(forms.ModelForm):
    class Meta:
        model = FinancialData
        fields = '__all__'  # You can specify specific fields here if needed

from django import forms
from .models import BusinessHouseData, BusinessHouseRelationship




class BusinessHouseRelationshipForm(forms.ModelForm):
    class Meta:
        model = BusinessHouseRelationship
        fields = ['from_business_house', 'to_business_house', 'relationship_type']
