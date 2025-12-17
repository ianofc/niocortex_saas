# secretariat/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ModeloDocumento, DocumentoEmitido
from .forms import ModeloDocumentoForm
from .services import SecretariatService
from pedagogical.models import Aluno

# --- MODELOS (TEMPLATES) ---

@login_required
def listar_modelos(request):
    modelos = ModeloDocumento.objects.filter(tenant_id=request.user.tenant_id)
    return render(request, 'secretariat/modelos/listar_modelos.html', {'modelos': modelos})

@login_required
def criar_modelo(request):
    if request.method == 'POST':
        form = ModeloDocumentoForm(request.POST)
        if form.is_valid():
            SecretariatService.create_template(request.user, form.cleaned_data)
            messages.success(request, "Modelo criado com sucesso!")
            return redirect('secretariat:listar_modelos')
    else:
        form = ModeloDocumentoForm()
    
    return render(request, 'secretariat/modelos/form_modelos.html', {'form': form, 'titulo': 'Novo Modelo de Documento'})

# --- EMISSÃO ---

@login_required
def selecionar_aluno_emissao(request):
    """ Passo 1: Listar alunos para escolher para quem emitir """
    alunos = Aluno.objects.filter(tenant_id=request.user.tenant_id)
    return render(request, 'secretariat/emissao/selecionar_aluno.html', {'alunos': alunos})

@login_required
def gerar_documento(request, aluno_id):
    """ Passo 2: Escolher o documento e gerar """
    aluno = get_object_or_404(Aluno, id=aluno_id, tenant_id=request.user.tenant_id)
    modelos = ModeloDocumento.objects.filter(tenant_id=request.user.tenant_id, ativo=True)
    
    if request.method == 'POST':
        modelo_id = request.POST.get('modelo_id')
        try:
            doc = SecretariatService.emitir_documento(request.user, aluno_id, modelo_id)
            messages.success(request, "Documento gerado!")
            return redirect('secretariat:visualizar_documento', doc_id=doc.id)
        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'secretariat/emissao/gerar_documento.html', {'aluno': aluno, 'modelos': modelos})

@login_required
def visualizar_documento(request, doc_id):
    """ Visualização final para impressão """
    documento = get_object_or_404(DocumentoEmitido, id=doc_id, tenant_id=request.user.tenant_id)
    return render(request, 'secretariat/emissao/visualizar_impressao.html', {'documento': documento})