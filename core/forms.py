# niocortex_saas/core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from uuid import uuid4

# Definir as Roles Freemium disponíveis no registro público
FREEMIUM_ROLES = [
    ('PROFESSOR_FREE', 'Professor (Gestão de Turmas - Limite 20 Alunos)'),
    ('ALUNO_FREE', 'Aluno (Homeschooling/Autoestudo - Acesso Vitalício)'),
]

class CustomUserCreationForm(UserCreationForm):
    """
    Formulário de Registro personalizado para o NioCortex Lumina.
    Permite ao usuário escolher sua role Freemium.
    """
    role_initial = forms.ChoiceField(
        choices=FREEMIUM_ROLES,
        label="Eu sou...",
        widget=forms.RadioSelect,
        initial='PROFESSOR_FREE' # Padrão: Professor
    )
    
    email = forms.EmailField(required=True, label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # Adicionamos 'email' e 'role_initial' aos campos padrão
        fields = UserCreationForm.Meta.fields + ('email', 'role_initial',)
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Este endereço de e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # 1. Atribui a Role e define como Usuário Individual (Freemium)
        user.role = self.cleaned_data.get('role_initial')
        user.tenant_type = 'INDIVIDUAL'
        
        if commit:
            user.save()
            # 2. CRÍTICO: Atribui o tenant_id do usuário como sendo o seu próprio ID
            # NOTA: O ID do Django User é um BigAutoField por padrão, mas para consistência com nosso modelo, 
            # usaremos o UUID gerado no momento da criação. No entanto, o ID primário é suficiente.
            # Se for necessário um UUID separado para o tenant_id, ajustaremos o save()
            
            # Usando o ID primário do usuário como o tenant_id inicial para freemium users:
            # user.tenant_id = user.id  # Isso não funciona com UUIDField se o ID não for UUID
            
            # Solução mais segura (usando o ID já gerado ou um novo UUID para o tenant_id):
            if not user.tenant_id:
                user.tenant_id = uuid4()
            
            user.save()
            
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """ Formulário de Login simples. """
    pass