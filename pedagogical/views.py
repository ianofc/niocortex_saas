# niocortex/pedagogical/views.py

import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Models e Forms
from .models import Turma, Aluno, Atividade, Nota
from .forms import TurmaForm, AlunoForm

# Services
from .services import PedagogicalService
from core.services.ai_client import AIClient

# ----------------------------------------------------------------------
# GESTÃO DE TURMAS
# ----------------------------------------------------------------------

@login_required
def listar_turmas_view(request):
    """ Exibe as turmas do professor (Free ou Corp) """
    try:
        turmas = PedagogicalService.list_turmas(request.user)
    except Exception as e:
        messages.error(request, f"Erro ao carregar turmas: {e}")
        turmas = []
    return render(request, 'pedagogical/turmas/listar_turmas.html', {'turmas': turmas})

@login_required
def criar_turma_view(request):
    """ Cria nova turma delegando validação de limites ao Serviço """
    if request.method == 'POST':
        form = TurmaForm(request.POST) 
        if form.is_valid():
            try:
                PedagogicalService.create_turma(request.user, form.cleaned_data)
                messages.success(request, "Turma criada com sucesso!")
                return redirect('pedagogical:listar_turmas')
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "Erro inesperado ao criar turma.")
    else:
        form = TurmaForm()

    return render(request, 'pedagogical/turmas/form_turmas.html', {
        'form': form,
        'titulo': 'Nova Turma',
        'btn_texto': 'Criar Turma'
    })

@login_required
def detalhe_turma(request, turma_id):
    """ Exibe o painel da turma (Dashboard da Turma) """
    try:
        turma = PedagogicalService.get_turma(request.user, turma_id)
        alunos = turma.alunos.all().order_by('nome')
    except PermissionDenied:
        messages.error(request, "Você não tem permissão para acessar esta turma.")
        return redirect('pedagogical:listar_turmas')

    return render(request, 'pedagogical/turmas/detalhar_turmas.html', {'turma': turma, 'alunos': alunos})

@login_required
def editar_turma(request, turma_id):
    try:
        turma = PedagogicalService.get_turma(request.user, turma_id)
    except PermissionDenied:
        return redirect('pedagogical:listar_turmas')

    if request.method == 'POST':
        form = TurmaForm(request.POST, instance=turma)
        if form.is_valid():
            form.save()
            messages.success(request, "Turma atualizada com sucesso.")
            return redirect('pedagogical:detalhe_turma', turma_id=turma.id)
    else:
        form = TurmaForm(instance=turma)
    
    return render(request, 'pedagogical/turmas/form_turmas.html', {
        'form': form, 
        'titulo': f'Editar {turma.nome}',
        'btn_texto': 'Salvar Alterações'
    })

@login_required
def excluir_turma(request, turma_id):
    """
    Remove uma turma do banco de dados.
    """
    # Exemplo de implementação real:
    # turma = get_object_or_404(Turma, id=turma_id)
    # turma.delete()
    
    # Por enquanto, apenas redireciona para evitar o erro
    print(f"Solicitação para excluir turma {turma_id}")
    return redirect('pedagogical:listar_turmas')

# ----------------------------------------------------------------------
# GESTÃO DE ALUNOS
# ----------------------------------------------------------------------

@login_required
def adicionar_aluno(request, turma_id):
    try:
        turma = PedagogicalService.get_turma(request.user, turma_id)
    except PermissionDenied:
        messages.error(request, "Turma não encontrada.")
        return redirect('pedagogical:listar_turmas')

    if request.method == 'POST':
        form = AlunoForm(request.user, request.POST) 
        if form.is_valid():
            try:
                PedagogicalService.add_aluno(
                    request.user, 
                    turma_id, 
                    form.cleaned_data
                )
                messages.success(request, "Aluno matriculado com sucesso!")
                return redirect('pedagogical:detalhe_turma', turma_id=turma.id)
            except ValidationError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Erro ao matricular: {e}")
    else:
        form = AlunoForm(request.user, initial={'turma': turma})
    
    return render(request, 'pedagogical/alunos/form_alunos.html', {
        'form': form, 
        'titulo': 'Novo Aluno',
        'subtitulo': f'Adicionando em: {turma.nome}'
    })

@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
    turma_origem_id = aluno.turma.id if aluno.turma else None

    if request.method == 'POST':
        form = AlunoForm(request.user, request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, "Dados do aluno atualizados.")
            if turma_origem_id:
                return redirect('pedagogical:detalhe_turma', turma_id=turma_origem_id)
            return redirect('pedagogical:listar_turmas')
    else:
        form = AlunoForm(request.user, instance=aluno)
    
    return render(request, 'pedagogical/alunos/form_alunos.html', {
        'form': form, 
        'titulo': f'Editar {aluno.nome}'
    })

@login_required
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
    turma_id = aluno.turma.id if aluno.turma else None

    if request.method == 'POST':
        aluno.delete()
        messages.success(request, "Aluno removido com sucesso.")
        if turma_id:
            return redirect('pedagogical:detalhe_turma', turma_id=turma_id)
        return redirect('pedagogical:listar_turmas')
    
    return render(request, 'pedagogical/alunos/exclusao_alunos.html', {
        'objeto': aluno,
        'voltar_para': turma_id
    })

# ----------------------------------------------------------------------
# GRADEBOOK & NOTAS (Matriz de Notas)
# ----------------------------------------------------------------------

@login_required
def gradebook(request, turma_id):
    """
    Recria a visão de Matriz de Notas.
    Mostra todos os alunos da turma e suas notas em cada atividade.
    """
    try:
        turma = PedagogicalService.get_turma(request.user, turma_id)
    except PermissionDenied:
        return redirect('pedagogical:listar_turmas')
    
    unidade = request.GET.get('unidade', '1ª Unidade')
    
    # 1. Buscar Atividades
    atividades = Atividade.objects.filter(
        turma=turma, 
        unidade=unidade,
        tenant_id=request.user.tenant_id
    ).order_by('data_aplicacao')
    
    # 2. Buscar Alunos
    alunos = turma.alunos.all().order_by('nome')
    
    # 3. Construir a Matriz de Notas
    notas = Nota.objects.filter(atividade__in=atividades, aluno__in=alunos)
    notas_map = {(n.aluno_id, n.atividade_id): n for n in notas}
    
    context = {
        'turma': turma,
        'atividades': atividades,
        'alunos': alunos,
        'notas_map': notas_map,
        'unidade_atual': unidade,
        'unidades_disponiveis': ['1ª Unidade', '2ª Unidade', '3ª Unidade', '4ª Unidade', 'Recuperação']
    }
    
    return render(request, 'pedagogical/gradebook/gradebook.html', context)

@login_required
@require_POST
def api_lancar_nota(request):
    """ Endpoint AJAX para salvar notas em tempo real """
    try:
        data = json.loads(request.body)
        aluno_id = data.get('aluno_id')
        atividade_id = data.get('atividade_id')
        valor = data.get('valor')

        if not aluno_id or not atividade_id:
            return JsonResponse({'status': 'error', 'message': 'IDs inválidos'}, status=400)

        aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
        atividade = get_object_or_404(Atividade, id=atividade_id, tenant_id=request.user.tenant_id)

        if valor is None or valor == "":
            Nota.objects.filter(aluno=aluno, atividade=atividade).delete()
            return JsonResponse({'status': 'success', 'message': 'Nota removida'})

        try:
            valor_decimal = float(valor)
            if valor_decimal < 0 or valor_decimal > atividade.valor_maximo:
                return JsonResponse({'status': 'error', 'message': f'Nota deve ser entre 0 e {atividade.valor_maximo}'}, status=400)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Valor numérico inválido'}, status=400)

        Nota.objects.update_or_create(
            aluno=aluno,
            atividade=atividade,
            tenant_id=request.user.tenant_id,
            defaults={'valor': valor_decimal}
        )

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# ----------------------------------------------------------------------
# API / IA - ANALYTICS (Integração com FastAPI)
# ----------------------------------------------------------------------

@login_required
def analisar_desempenho_aluno(request, aluno_id):
    """
    Endpoint AJAX para solicitar análise do aluno ao microsserviço de IA.
    """
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Método não permitido"}, status=405)

    try:
        aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
        
        # Busca histórico real para enviar à IA
        notas_recentes = Nota.objects.filter(aluno=aluno).order_by('-atividade__data_aplicacao')[:5]
        lista_notas = [float(n.valor) for n in notas_recentes if n.valor is not None]
        
        dados_preparados = {
            "nome": aluno.nome,
            "turma": aluno.turma.nome if aluno.turma else "Sem Turma",
            "notas": lista_notas, 
            "obs": ["Solicitação manual via dashboard do professor."]
        }

        resultado_ia = AIClient.analisar_aluno(dados_preparados)

        if "error" in resultado_ia:
            return JsonResponse({"status": "error", "message": resultado_ia["error"]}, status=503)

        return JsonResponse({
            "status": "success",
            "data": resultado_ia
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

# ======================================================================
# ZONA DE INTELIGÊNCIA ARTIFICIAL (COPILOTO PEDAGÓGICO)
# ======================================================================

# --- 1. GERADOR DE PROVAS ---

@login_required
def view_gerador_provas(request):
    """ Renderiza a tela do Gerador de Avaliações """
    turmas = PedagogicalService.list_turmas(request.user)
    return render(request, 'pedagogical/ferramentas/gerador_provas.html', {'turmas': turmas})

@login_required
@require_POST
def api_gerar_prova(request):
    """
    Recebe os parâmetros do professor e chama a IA para criar a prova.
    """
    try:
        data = json.loads(request.body)
        
        if not data.get('tema'):
            return JsonResponse({'status': 'error', 'message': 'O tema é obrigatório.'}, status=400)

        # Contexto da turma
        nivel_ensino = "Geral"
        if data.get('turma_id'):
            turma = get_object_or_404(Turma, id=data['turma_id'], tenant_id=request.user.tenant_id)
            nivel_ensino = turma.nome

        # Payload para IA
        payload_ia = {
            "tema": data['tema'],
            "nivel": nivel_ensino,
            "dificuldade": data.get('dificuldade', 'Médio'),
            "qtd_questoes": int(data.get('quantidade', 5)),
            "tipo_questoes": data.get('tipos', ['Múltipla Escolha']),
            "instrucoes_extras": "Gere em formato HTML limpo para renderização web."
        }

        resultado = AIClient.gerar_prova(payload_ia)

        if 'error' in resultado:
            return JsonResponse({'status': 'error', 'message': resultado['error']}, status=503)

        return JsonResponse({
            'status': 'success',
            'prova_conteudo': resultado.get('conteudo', ''),
            'gabarito': resultado.get('gabarito', '')
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# --- 2. GERADOR DE PLANEJAMENTOS (PLANOS DE AULA) ---

@login_required
def view_gerador_planejamentos(request):
    """ Tela para criar Planos de Aula com IA """
    turmas = PedagogicalService.list_turmas(request.user)
    return render(request, 'pedagogical/ferramentas/gerador_planejamentos.html', {'turmas': turmas})

@login_required
@require_POST
def api_gerar_planejamento(request):
    """
    Gera roteiro de aula alinhado à BNCC.
    """
    try:
        data = json.loads(request.body)
        
        if not data.get('tema'):
            return JsonResponse({'status': 'error', 'message': 'O tema é obrigatório.'}, status=400)

        nivel = "Geral"
        if data.get('turma_id'):
            turma = get_object_or_404(Turma, id=data['turma_id'], tenant_id=request.user.tenant_id)
            nivel = turma.nome

        payload_ia = {
            "tema": data.get('tema'),
            "disciplina": data.get('disciplina', 'Geral'),
            "nivel": nivel,
            "duracao": data.get('duracao', '1 hora aula'),
            "metodologia": data.get('metodologia', 'Ativa'),
            "instrucoes_extras": "Incorpore códigos da BNCC."
        }

        resultado = AIClient.gerar_plano_aula(payload_ia)

        if 'error' in resultado:
            return JsonResponse({'status': 'error', 'message': resultado['error']}, status=503)

        return JsonResponse({
            'status': 'success',
            'plano': resultado.get('conteudo', ''),
            'bncc': resultado.get('codigos_bncc', [])
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# --- 3. GERADOR DE ATIVIDADES (EXERCÍCIOS) ---

@login_required
def view_gerador_atividades(request):
    """ Tela para criar Listas de Exercícios / Dinâmicas """
    turmas = PedagogicalService.list_turmas(request.user)
    return render(request, 'pedagogical/ferramentas/gerador_atividades.html', {'turmas': turmas})

@login_required
@require_POST
def api_gerar_atividade(request):
    """
    Gera exercícios rápidos ou dinâmicas.
    """
    try:
        data = json.loads(request.body)
        
        if not data.get('tema'):
            return JsonResponse({'status': 'error', 'message': 'O tema é obrigatório.'}, status=400)

        nivel = "Geral"
        if data.get('turma_id'):
            turma = get_object_or_404(Turma, id=data['turma_id'], tenant_id=request.user.tenant_id)
            nivel = turma.nome

        payload_ia = {
            "tema": data.get('tema'),
            "nivel": nivel,
            "ludico": data.get('estilo') == 'Ludico', # Ex: Caça-palavras, Jogos
            "instrucoes_extras": "Gere pronto para imprimir ou projetar."
        }

        resultado = AIClient.gerar_atividade(payload_ia)

        if 'error' in resultado:
            return JsonResponse({'status': 'error', 'message': resultado['error']}, status=503)

        return JsonResponse({
            'status': 'success',
            'conteudo': resultado.get('conteudo', '')
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def listar_turmas(request):
    return render(request, 'pedagogical/turmas/listar_turmas.html')

@login_required
def form_turmas(request):
    return render(request, 'pedagogical/turmas/form_turmas.html')

@login_required
def detalhar_turma(request, turma_id):
    return render(request, 'pedagogical/turmas/detalhar_turmas.html')

@login_required
def gerador_planejamentos(request):
    return render(request, 'pedagogical/ferramentas/gerador_planejamentos.html')

@login_required
def gerador_atividades(request):
    return render(request, 'pedagogical/ferramentas/gerador_atividades.html')

@login_required
def gerador_provas(request):
    return render(request, 'professor/avaliacoes/gerador_provas.html')

@login_required
def gradebook_view(request):
    return render(request, 'pedagogical/gradebook/gradebook.html')

@login_required
def excluir_turma(request, turma_id):
    print(f"Solicitação para excluir turma {turma_id}")
    return redirect('pedagogical:listar_turmas')

@login_required
def listar_alunos(request):
    return render(request, 'pedagogical/alunos/listar_alunos.html')

@login_required
def form_alunos(request):
    return render(request, 'pedagogical/alunos/form_alunos.html')

@login_required
def exclusao_alunos(request, aluno_id):
    return redirect('pedagogical:listar_alunos')