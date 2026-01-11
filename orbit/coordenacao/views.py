from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import PlanejamentoAula, OcorrenciaDisciplinar
from lumenios.pedagogico.models import Aluno, Turma

@login_required
def dashboard_coordenacao(request):
    """ Painel Visão Geral da Coordenação """
    # Se precisar filtrar por tenant no futuro:
    # tenant_id = request.user.tenant_id 
    
    # Mock de dados (ou queries reais se já tiver dados)
    # Contagem de alunos, se o model Aluno estiver populado
    total_alunos = Aluno.objects.count()
    
    # Exemplo de queries reais (ajuste conforme necessidade)
    planos_pendentes = PlanejamentoAula.objects.filter(status='ENVIADO').count()
    ocorrencias_hoje = OcorrenciaDisciplinar.objects.filter(data_ocorrencia__date__gte="2025-01-01").count() # Exemplo
    
    context = {
        'total_alunos': total_alunos,
        'planos_pendentes': planos_pendentes,
        'ocorrencias_hoje': 3, # Valor fixo por enquanto se não tiver dados
        'frequencia_media': '94%',
        
        # Listas para as tabelas
        'ultimos_planos': PlanejamentoAula.objects.select_related('professor', 'disciplina').order_by('-created_at')[:5],
    }
    
    return render(request, 'coordenacao/dashboard/visao_geralcoord.html', context)