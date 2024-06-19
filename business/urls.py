from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.loan_self_investment, name='loan_self_investment'),
    path('success/', views.success_url, name='success_url'),
    path('investment/<int:investment_id>/', views.investment_details, name='investment_details'),
    path('', views.businesshouse_list, name='businesshouse_list'),
    path('house/<int:pk>/', views.businesshouse_detail, name='businesshouse_detail'),
    path('houses/add/', views.add_businesshouse, name='add_businesshouse'),
    path('houses/<int:pk>/delete/', views.delete_businesshouse, name='businesshouse_delete'),
    path('financial_input/', views.financial_input, name='financial_input'),
    path('financial_output/<int:business_house_id>/', views.financial_output, name='financial_output'),
]
