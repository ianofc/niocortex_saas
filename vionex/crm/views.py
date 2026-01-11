from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Lead, Oportunidade, FunilEtapa, AtividadeCRM
from .forms import LeadForm, OportunidadeForm, AtividadeForm

@login_required
def dashboard_crm(request):
    """ Visão Geral do Pipeline (Kanban) """
    etapas = FunilEtapa.objects.filter(tenant_id=request.user.tenant_id).prefetch_related('oportunidades__lead')
    
    # KPIs Rápidos
    total_aberto = Oportunidade.objects.filter(tenant_id=request.user.tenant_id, status='ABERTO').aggregate(Sum('valor_estimado'))['valor_estimado__sum'] or 0
    total_ganho = Oportunidade.objects.filter(tenant_id=request.user.tenant_id, status='GANHO').count()
    
    return render(request, 'crm_sales/dashboard.html', {
        'etapas': etapas,
        'total_pipeline': total_aberto,
        'leads_convertidos': total_ganho
    })

@login_required
def listar_leads(request):
    leads = Lead.objects.filter(tenant_id=request.user.tenant_id).order_by('-created_at')
    return render(request, 'crm_sales/leads/listar_leads.html', {'leads': leads})

@login_required
def novo_lead(request):
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.tenant_id = request.user.tenant_id
            lead.responsavel = request.user
            lead.save()
            messages.success(request, "Lead cadastrado!")
            return redirect('vionex_crm:listar_leads')
    else:
        form = LeadForm()
    return render(request, 'crm_sales/leads/form_leads.html', {'form': form, 'titulo': 'Novo Lead'})

@login_required
def detalhe_oportunidade(request, op_id):
    oportunidade = get_object_or_404(Oportunidade, id=op_id, tenant_id=request.user.tenant_id)
    atividades = oportunidade.atividades.all()
    
    if request.method == 'POST':
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.tenant_id = request.user.tenant_id
            atividade.oportunidade = oportunidade
            atividade.usuario = request.user
            atividade.save()
            messages.success(request, "Atividade registrada.")
            return redirect('vionex_crm:detalhe_oportunidade', op_id=op_id)
    else:
        form = AtividadeForm()

    return render(request, 'crm_sales/oportunidades/detalhe.html', {
        'oportunidade': oportunidade,
        'atividades': atividades,
        'form_atividade': form
    })