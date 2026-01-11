from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import MetaInstitucional, ReuniaoEstrategica
# Importar modelos de outros módulos para gerar os KPIs
from lumenios.pedagogico.models import Aluno
from ledger.financeiro.models import BoletoAluno

@login_required
def dashboard_direcao(request):
    """ 
    Cockpit da Direção: Visão 360º da Escola.
    """
    # 1. KPIs Financeiros (Resumo)
    faturamento_previsto = BoletoAluno.objects.filter(status='PENDENTE').aggregate(Sum('valor'))['valor__sum'] or 0
    faturamento_realizado = BoletoAluno.objects.filter(status='PAGO').aggregate(Sum('valor'))['valor__sum'] or 0
    inadimplencia_count = BoletoAluno.objects.filter(status='VENCIDO').count()

    # 2. KPIs Pedagógicos/Comerciais
    total_alunos = Aluno.objects.count()
    # Exemplo: Alunos ativos vs capacidade (mock)
    capacidade_escola = 1500 
    ocupacao = int((total_alunos / capacidade_escola) * 100) if capacidade_escola > 0 else 0

    # 3. Metas Estratégicas
    metas = MetaInstitucional.objects.filter(tenant_id=request.user.tenant_id).order_by('prazo')

    # 4. Próximas Reuniões
    reunioes = ReuniaoEstrategica.objects.filter(tenant_id=request.user.tenant_id).order_by('-data')[:3]

    context = {
        'kpi_financeiro': {
            'previsto': faturamento_previsto,
            'realizado': faturamento_realizado,
            'inadimplencia_qtd': inadimplencia_count
        },
        'kpi_escola': {
            'total_alunos': total_alunos,
            'ocupacao': ocupacao
        },
        'metas': metas,
        'reunioes': reunioes
    }
    
    # Reutiliza o template de dashboard corporativo ou cria um específico em prioris
    return render(request, 'prioris_direcao/dashboard.html', context)