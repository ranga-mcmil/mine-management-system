from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mine_mgt'

urlpatterns = [
   # post views
   path('', views.dashboard, name='dashboard'),
   path('payments/', views.payments, name='payments'),
   path('claim/<int:id>', views.claim_detail, name='claim_detail'),
   path('application/<int:id>', views.claim_application, name='claim_application'),
   path('accept/<int:id>', views.accept, name='accept'),
   path('apply/', views.apply, name='apply'),
   path('forfeited/<int:id>', views.forfeited, name='forfeited'),
   path('apply_forfeited/<int:id>', views.apply_forfeited, name='apply_forfeited'),
   path('delete_forfeited/<int:id>', views.delete_forfeited, name='delete_forfeited'),
   path('add_payment/<int:id>', views.add_payment, name='add_payment'),
   path('claims_on_offer/', views.claims_on_offer, name='claims_on_offer'),
   path('declined/<int:id>', views.declined, name='declined'),
   path('add_annual_inspection/', views.add_annual_inspection, name='add_annual_inspection'),
   path('annual_inspections/', views.annual_inspections, name='annual_inspections'),
   path('accept2/<int:id>', views.accept2, name='accept2'),
   

]