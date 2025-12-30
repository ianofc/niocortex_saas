# niocortex/financial/forms.py

from django import forms
from .models import ContratoAluno
from lumenios.pedagogico.models import Aluno
from .models import Fornecedor, Patrimonio

# --- GESTÃO DE COMPRAS E PATRIMÓNIO ---

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['razao_social', 'cnpj', 'categoria', 'telefone', 'aprovado_licitacao']
        widgets = {
            'razao_social': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome da Empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '00.000.000/0000-00'}),
            'categoria': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Informática, Limpeza'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'aprovado_licitacao': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-[#6200EA]'}),
        }

class PatrimonioForm(forms.ModelForm):
    class Meta:
        model = Patrimonio
        fields = ['codigo_etiqueta', 'descricao', 'data_aquisicao', 'valor_compra', 'vida_util_anos', 'estado_conservacao']
        widgets = {
            'codigo_etiqueta': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ETQ-00001'}),
            'descricao': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Projetor Epson X50'}),
            'data_aquisicao': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'valor_compra': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'vida_util_anos': forms.NumberInput(attrs={'class': 'form-input'}),
            'estado_conservacao': forms.Select(attrs={'class': 'form-select'}),
        }

class ContratoAlunoForm(forms.ModelForm):
    """
    Formulário para criar ou editar contratos financeiros de alunos.
    """
    class Meta:
        model = ContratoAluno
        fields = [
            'aluno', 
            'responsavel_financeiro', 'cpf_cnpj_responsavel',
            'valor_mensalidade', 'dia_vencimento'
        ]
        widgets = {
            'aluno': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] outline-none'
            }),
            'responsavel_financeiro': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] outline-none',
                'placeholder': 'Nome completo do responsável'
            }),
            'cpf_cnpj_responsavel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] outline-none', 
                'placeholder': 'CPF ou CNPJ'
            }),
            'valor_mensalidade': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] outline-none', 
                'step': '0.01'
            }),
            'dia_vencimento': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] outline-none', 
                'min': 1, 
                'max': 31
            }),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # Filtra o dropdown para mostrar apenas alunos da escola atual (Tenant Isolation)
            self.fields['aluno'].queryset = Aluno.objects.filter(tenant_id=user.tenant_id).order_by('nome')

class GerarBoletoForm(forms.Form):
    """ 
    Formulário para geração manual de boletos avulsos (Ex: Venda de uniforme, taxa extra).
    """
    referencia = forms.CharField(
        label="Referência / Descrição",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] outline-none',
            'placeholder': 'Ex: Material Didático 2025'
        })
    )
    valor = forms.DecimalField(
        label="Valor (R$)",
        max_digits=10, 
        decimal_places=2,
        required=False, # Se vazio, usa o valor da mensalidade padrão
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] outline-none',
            'placeholder': 'Deixe vazio para usar o valor do contrato'
        })
    )