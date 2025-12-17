# hr/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Funcionario, Departamento, Cargo
from .forms import FuncionarioForm, DepartamentoForm, CargoForm
from .services import HRService

# --- FUNCIONÁRIOS ---

@login_required
def listar_funcionarios(request):
    funcionarios = HRService.list_employees(request.user)
    return render(request, 'hr/funcionarios/listar_funcionarios.html', {'funcionarios': funcionarios})

@login_required
def criar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.user, request.POST)
        if form.is_valid():
            try:
                HRService.create_employee(request.user, form.cleaned_data)
                messages.success(request, "Funcionário cadastrado com sucesso!")
                return redirect('hr:listar_funcionarios')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = FuncionarioForm(request.user)
    
    return render(request, 'hr/funcionarios/form_funcionarios.html', {
        'form': form, 'titulo': 'Novo Colaborador'
    })

# --- DEPARTAMENTOS ---

@login_required
def listar_departamentos(request):
    departamentos = Departamento.objects.filter(tenant_id=request.user.tenant_id)
    return render(request, 'hr/departamentos/listar_departamentos.html', {'departamentos': departamentos})

@login_required
def criar_departamento(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.user, request.POST)
        if form.is_valid():
            HRService.create_department(request.user, form.cleaned_data)
            messages.success(request, "Departamento criado!")
            return redirect('hr:listar_departamentos')
    else:
        form = DepartamentoForm(request.user)
    
    return render(request, 'hr/departamentos/form_departamentos.html', {'form': form, 'titulo': 'Novo Departamento'})

# --- CARGOS ---

@login_required
def listar_cargos(request):
    cargos = Cargo.objects.filter(tenant_id=request.user.tenant_id)
    return render(request, 'hr/cargos/listar_cargos.html', {'cargos': cargos})

@login_required
def criar_cargo(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            HRService.create_position(request.user, form.cleaned_data)
            messages.success(request, "Cargo criado!")
            return redirect('hr:listar_cargos')
    else:
        form = CargoForm()
    
    return render(request, 'hr/cargos/form_cargos.html', {'form': form, 'titulo': 'Novo Cargo'})