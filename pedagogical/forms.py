# niocortex/pedagogical/forms.py

from django import forms
from .models import Turma, Aluno

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'ano_letivo']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] focus:border-transparent outline-none',
                'placeholder': 'Ex: 9º Ano A'
            }),
            'ano_letivo': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] focus:border-transparent outline-none',
                'value': 2025
            })
        }

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        # CORREÇÃO: 'matricula_id' deve corresponder ao campo no models.py
        fields = ['nome', 'matricula_id', 'turma']
        labels = {
            'matricula_id': 'Matrícula'
        }
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] focus:border-transparent outline-none',
                'placeholder': 'Nome do Aluno'
            }),
            'matricula_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] focus:border-transparent outline-none',
                'placeholder': 'Ex: 2024001'
            })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # TRUQUE DE SEGURANÇA: Importação local para evitar Circular Import com services.py
        from .services import PedagogicalService
        
        # O professor só pode ver as turmas DELE no dropdown (Filtragem por Tenant)
        if user:
            self.fields['turma'].queryset = PedagogicalService.list_turmas(user)
        
        # Estilização Tailwind para o Select (que é renderizado via {{ form.turma }} no template)
        self.fields['turma'].widget.attrs.update({
            'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white focus:ring-2 focus:ring-[#6200EA] focus:border-transparent outline-none'
        })