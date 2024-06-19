# urls.py
from django.urls import path
from bank_interest import views
from .views import UploadBankInterestCsv



urlpatterns = [
    path('', views.home, name='home'),
    path('transaction', views.transaction_create, name='transaction_create'),
    path('bank_interest/', views.bank_interest_list, name='bank_interest_list'),
    path('bank_interest/add/', views.add_bank_interest, name='add_bank_interest'),
    path('bank_interest/edit/<int:pk>/', views.edit_bank_interest, name='edit_bank_interest'),
    path('bank_interest/delete/<int:pk>/', views.delete_bank_interest, name='delete_bank_interest'),
    path('bank_transaction/', views.bank_transaction, name='bank_transaction'),


    # path('forex/', views.forex_view, name='forex_view'),
    path('forex/today/', views.forex_today, name='forex_today'),
    path('forex/yesterday/', views.forex_yesterday, name='forex_yesterday'),




    path('success/<int:transaction_id>/', views.success_page, name='success_page'),


    path('upload_bank_interest_csv/', UploadBankInterestCsv.as_view(), name='upload_bank_interest_csv'),




]


