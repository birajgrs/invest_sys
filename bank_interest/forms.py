from django import forms
from .models import BankInterest,BankTransaction
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = "date"

class BankInterestForm(forms.ModelForm):
    current_year = datetime.now().year
    year_range = range(current_year, current_year + 10)

    from_date = forms.DateField(
        widget=forms.SelectDateWidget(
            years=year_range,
            empty_label=("Choose Year", "Choose Month", "Choose Day")
        ),
        input_formats=['%Y-%m-%d']
    )

    class Meta:
        model = BankInterest
        fields = ['bank_name', 'deposit_type', 'interest_rate', 'from_date']


class BankInterestCSVForm(forms.ModelForm):
    class Meta:
        model = BankInterest
        fields = ['bank_name', 'deposit_type', 'interest_rate', 'from_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom initialization if needed

    def save_from_csv_row(self, row):
        """
        Create a BankInterest instance from a CSV row.
        Assumes the row has the format: bank_name, deposit_type, interest_rate, from_date
        """
        bank_name, deposit_type, interest_rate, from_date = row
        # You might need to do additional parsing or data conversion here
        self.instance.bank_name = bank_name
        self.instance.deposit_type = deposit_type
        self.instance.interest_rate = interest_rate
        self.instance.from_date = from_date
        self.instance.save()




class InterestCalculationForm(forms.ModelForm):
    future_date = forms.DateField(widget=forms.SelectDateWidget(years=range(datetime.now().year, datetime.now().year + 10)))

    class Meta:
        model = BankTransaction
        fields = ['amount', 'bank_name', 'deposit_type', 'future_date']

