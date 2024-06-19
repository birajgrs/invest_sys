import csv
import logging
from datetime import date
from rest_framework import status
from django.urls import reverse
from django.contrib import messages
from .forms import  BankInterestForm
from django.http import HttpResponseRedirect
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BankTransaction, BankInterest
from .forms import InterestCalculationForm
from api.forex_api import get_forex_rates
from django.shortcuts import render, redirect, get_object_or_404




# Configure logging
logging.basicConfig(level=logging.DEBUG)

def home(request):
    return render(request, 'base.html')


def bank_interest_list(request):
    bank_interests = BankInterest.objects.all()
    return render(request, 'bank_interest/bank_interest_list.html', {'bank_interests': bank_interests})



def add_bank_interest(request):
    if request.method == 'POST':
        form = BankInterestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bank_interest_list')
    else:
        form = BankInterestForm()
    return render(request, 'bank_interest/add_bank_interest.html', {'form': form})

def edit_bank_interest(request, pk):
    bank_interest = BankInterest.objects.get(pk=pk)
    if request.method == 'POST':
        form = BankInterestForm(request.POST, instance=bank_interest)
        if form.is_valid():
            form.save()
            return redirect('bank_interest_list')
    else:
        form = BankInterestForm(instance=bank_interest)
    return render(request, 'bank_interest/edit_bank_interest.html', {'form': form})



def delete_bank_interest(request, pk):
    bank_interest = BankInterest.objects.get(pk=pk)
    bank_interest.delete()
    return HttpResponseRedirect(reverse('bank_interest_list'))




def transaction_create(request):
    return render(request, 'deposit_or_loan.html')





from django.shortcuts import render
from datetime import datetime, timedelta
from api.forex_api import get_forex_rates  # Ensure you have a utility function to fetch the Forex rates

def forex_today(request):
    date = datetime.now().strftime('%Y-%m-%d')
    forex_data = get_forex_rates(date)

    context = {
        'forex_data': forex_data['data']['payload'][0]['rates'] if forex_data and forex_data['data']['payload'] else None,
        'date': date,
    }
    return render(request, 'forex/forex.html', context)

def forex_yesterday(request):
    date = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    forex_data = get_forex_rates(date)

    context = {
        'forex_data': forex_data['data']['payload'][0]['rates'] if forex_data and forex_data['data']['payload'] else None,
        'date': date,
    }
    return render(request, 'forex/forex.html', context)




















class UploadBankInterestCsv(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, format=None):
        file_obj = request.FILES.get('csv_file')

        if not file_obj:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_file)
            next(csv_reader)  # Skip header row

            for row in csv_reader:
                bank_name, deposit_type, interest_rate, from_date = row
                
                # Create or update BankInterest object
                BankInterest.objects.update_or_create(
                    bank_name=bank_name,
                    deposit_type=deposit_type,
                    defaults={
                        'interest_rate': float(interest_rate.strip('%')),
                        'from_date': from_date
                    }
                )

            return Response({'message': 'Data inserted successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import InterestCalculationForm
from .models import BankInterest, BankTransaction
from django.contrib import messages


def bank_transaction(request):
    if request.method == 'POST':
        form = InterestCalculationForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            bank_name = form.cleaned_data['bank_name']
            deposit_type = form.cleaned_data['deposit_type']
            future_date = form.cleaned_data['future_date']
            current_date = date.today()


            # Get all BankInterest objects matching bank_name and deposit_type
            rates_and_dates = BankInterest.objects.filter(
                bank_name=bank_name,
                deposit_type=deposit_type
            )

            days,total_interest, total_amount = calculate_interest(amount, rates_and_dates, future_date,current_date)

            transaction = BankTransaction.objects.create(
                future_date=future_date,
                bank_name=bank_name,
                deposit_type=deposit_type,
                amount=amount,
                total_amount=total_amount,
                total_interest=total_interest,
                days = days,
            )

            return redirect(reverse('success_page', kwargs={'transaction_id': transaction.id}))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = InterestCalculationForm()

    bank_names = BankInterest.objects.values_list('bank_name', flat=True).distinct()
    deposit_types = BankInterest.objects.values_list('deposit_type', flat=True).distinct()

    return render(request, 'user_input/Bank_form.html', {'form': form, 'bank_names': bank_names, 'deposit_types': deposit_types})

def success_page(request, transaction_id):
    try:
        transaction = get_object_or_404(BankTransaction, pk=transaction_id)
    except (BankTransaction.DoesNotExist, ValueError):
        messages.error(request, "Invalid transaction ID.")
        return redirect('error_page')
    
    context = {
        'date': transaction.future_date,
        'bank_name': transaction.bank_name,
        'deposit_type': transaction.deposit_type,
        'amount': transaction.amount,
        'total_amount': transaction.total_amount,
        'total_interest': transaction.total_interest,
        'days': transaction.days,
    }
    return render(request, 'success.html', {'transaction': transaction, 'context': context})


from datetime import date

def calculate_interest(amount, rates_and_dates, future_date, current_date):
    total_interest = 0
    total_amount = amount

    # Iterate through each rate and date pair
    for rate_and_date in rates_and_dates:
        rate = rate_and_date.interest_rate
        date = rate_and_date.from_date

        # Calculate the number of days between current date and the next date
        days = (date - current_date).days
        # days = 100

        # Calculate interest for the current period
        interest = total_amount * rate / 100 / 365 * days

        # Update total interest and total amount
        total_interest += interest
        total_amount += interest
        days  += days

        # Update current date to the next date
        current_date = date

        # If the current date exceeds the future date, break the loop
        if current_date >= future_date:
            break

    return days, total_interest, total_amount



































































































































# def calculate_interest(amount, rates_and_dates, future_date):
#     total_interest = 0
#     total_amount = amount
#     current_date = date.today()
#  # Assuming from_date is the field name for the date
    
#     # Iterate through each rate and date pair
#     for rate_and_date in rates_and_dates:
#         rate = rate_and_date.interest_rate  # Assuming interest_rate is the field name for the rate
#         date = rate_and_date.from_date  # Assuming from_date is the field name for the date
        
#         # Calculate the number of days between current date and the next date
#         days = (date - current_date).days
        
#         # Calculate interest for the current period
#         interest = total_amount * rate / 100 / 365 * days
        
#         # Update total interest and total amount
#         total_interest += interest
#         total_amount += interest
        
#         # Update current date to the next date
#         current_date = date
    
#         # If the current date exceeds the future date, break the loop
#         if current_date > future_date:
#             break
    
#     return total_interest, total_amount




# def bank_transaction(request):
#     if request.method == 'POST':
#         form = InterestCalculationForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             bank_name = form.cleaned_data['bank_name']
#             deposit_type = form.cleaned_data['deposit_type']
#             future_date = form.cleaned_data['future_date']

#             # Get all BankInterest objects matching bank_name and deposit_type
#             rates_and_dates = BankInterest.objects.filter(
#                 bank_name=bank_name,
#                 deposit_type=deposit_type
#             )

#             total_interest, total_amount = calculate_interest(amount, rates_and_dates, future_date)


#             transaction = BankTransaction.objects.create(
#                 future_date=future_date,
#                 bank_name=bank_name,
#                 deposit_type=deposit_type,
#                 amount=amount,
#                 total_amount=total_amount,
#                 total_interest=total_interest,
#             )

#             return redirect(reverse('success_page', kwargs={'transaction_id': transaction.id}))
#         else:
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"Error in {field}: {error}")
#     else:
#         form = InterestCalculationForm()

#     bank_names = BankInterest.objects.values_list('bank_name', flat=True).distinct()
#     deposit_types = BankInterest.objects.values_list('deposit_type', flat=True).distinct()

#     return render(request, 'user_input/Bank_form.html', {'form': form, 'bank_names': bank_names, 'deposit_types': deposit_types})





# def success_page(request, transaction_id):
#     try:
#         transaction = get_object_or_404(BankTransaction, pk=transaction_id)
#     except BankTransaction.DoesNotExist:
#         messages.error(request, "Transaction does not exist.")
#         return redirect('error_page')
    
#     context = {
#         'date': transaction.future_date,
#         'bank_name': transaction.bank_name,
#         'deposit_type': transaction.deposit_type,
#         'amount': transaction.amount,
#         'total_amount':transaction.total_amount,
#         'total_interest':transaction.total_interest,

#     }
#     return render(request, 'success.html', {'transaction': transaction, 'context': context})




