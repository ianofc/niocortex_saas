# niocortex/crm_sales/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def crm_dashboard(request):
    """ Dashboard temporário do CRM """
    return render(request, 'crm_sales/dashboard.html', {})