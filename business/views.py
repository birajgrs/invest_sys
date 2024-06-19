

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import SelfBankInvestmentForm, BusinessHouseForm, FinancialDataForm, BusinessHouseRelationshipForm
from .models import SelfBankInvestment, BusinessHouseData, FinancialData, BusinessHouseRelationship
from exportcode import distribution

def loan_self_investment(request):
    if request.method == 'POST':
        form = SelfBankInvestmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = SelfBankInvestmentForm()
    return render(request, 'business/loan_self_invest.html', {'form': form})

def success_url(request):
    investments = SelfBankInvestment.objects.all().order_by('-id')
    return render(request, 'business/success.html', {'investments': investments})

def investment_details(request, investment_id):
    investment = get_object_or_404(SelfBankInvestment, pk=investment_id)
    if request.method == 'POST' and 'delete' in request.POST:
        investment.delete()
        return redirect('success_url')
    return render(request, 'business/investment_details.html', {'investment': investment})

def delete_businesshouse(request, pk):
    businesshouse = get_object_or_404(BusinessHouseData, pk=pk)
    if request.method == 'POST':
        businesshouse.delete()
        return redirect('businesshouse_list')

def businesshouse_list(request):
    businesshouses = BusinessHouseData.objects.all()
    return render(request, 'business/dynamic_business.html', {'businesshouses': businesshouses})

def businesshouse_detail(request, pk):
    businesshouse = get_object_or_404(BusinessHouseData, pk=pk)
    return render(request, 'business/dynamic_business.html', {'businesshouse': businesshouse})

def add_businesshouse(request):
    if request.method == 'POST':
        form = BusinessHouseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('businesshouse_list')
    else:
        form = BusinessHouseForm()
    return render(request, 'business/dynamic_business.html', {'form': form})

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import FinancialDataForm, BusinessHouseRelationshipForm
from .models import BusinessHouseData

def financial_input(request):
    financial_form = FinancialDataForm()
    relationship_form = BusinessHouseRelationshipForm()

    if request.method == 'POST':
        if 'financial_form_submit' in request.POST:
            financial_form = FinancialDataForm(request.POST)
            if financial_form.is_valid():
                financial_form.save()
                return redirect('financial_input')
        elif 'relationship_form_submit' in request.POST:
            relationship_form = BusinessHouseRelationshipForm(request.POST)
            if relationship_form.is_valid():
                relationship_form.save()
                return redirect('financial_input')

    business_housesall = BusinessHouseData.objects.all()
    selected_business_house_id = request.GET.get('business_house_id')

    if selected_business_house_id:
        return HttpResponseRedirect(reverse('financial_output', args=[selected_business_house_id]))

    return render(request, 'business/financial_input.html', {
        'financial_form': financial_form,
        'relationship_form': relationship_form,
        'business_houses': business_housesall,
        'selected_business_house_id': selected_business_house_id,
    })

def calculate_financials(business_house_id):
    business_house = get_object_or_404(BusinessHouseData, pk=business_house_id)
    financial_data = business_house.financial_data.all()
    
    sectors = []
    for data in financial_data:
        sector = {
            "name": business_house.name,
            "other_expenses": data.daily_expenses_extra,
            "paid_for_nea": data.daily_income,
        }
        sectors.append(sector)
    
    sectors = distribution.adjust_distribution(sectors)
    
    try:
        roi_time, npv, profitability_index = distribution.calculate_combined_values(
            sectors,
            business_house.total_investment,
            business_house.discount_rate,
            business_house.operational_days,
            business_house.project_lifetime
        )
    except OverflowError:
        roi_time = npv = profitability_index = float('inf')

    return {
        "business_house": business_house,
        "financial_data": financial_data,
        "roi_time": roi_time,
        "npv": npv,
        "profitability_index": profitability_index,
        "sectors": sectors
    }

def financial_output(request, business_house_id):
    context = calculate_financials(business_house_id)
    return render(request, 'business/financial_output.html', context)
