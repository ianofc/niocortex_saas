
from django import forms
from .models import Turma, Aluno

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'ano_letivo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-all outline-none',
                'placeholder': 'Ex: 3º Ano A'
            }),
            'ano_letivo': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 text-gray-900 focus:ring-2 focus:ring-yellow-500 focus:border-transparent transition-all outline-none',
                'placeholder': '2025'
            }),
        }

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula_id', 'email', 'telefone_responsavel']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': 'Nome Completo'
            }),
            'matricula_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': 'Matrícula (Opcional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': 'email@exemplo.com'
            }),
            'telefone_responsavel': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 border border-gray-200 focus:ring-2 focus:ring-indigo-500 outline-none',
                'placeholder': '(XX) 9XXXX-XXXX'
            }),
        }
