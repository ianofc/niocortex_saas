from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

# --- MODELOS NOVOS (GALERIA) ---

class Album(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='albuns')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    privacidade = models.CharField(max_length=20, default='PUBLIC', choices=[
        ('PUBLIC', 'Público'), ('FRIENDS', 'Amigos'), ('PRIVATE', 'Privado')
    ])
    def __str__(self): return f"{self.titulo} - {self.usuario}"

class UserMedia(models.Model):
    TIPO_USO = [('PERFIL', 'Foto de Perfil'), ('CAPA', 'Foto de Capa'), ('FEED', 'Postagem no Feed'), ('ALBUM', 'Item de Álbum')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='midias')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='itens')
    arquivo = models.FileField(upload_to='user_media/%Y/%m/')
    tipo_arquivo = models.CharField(max_length=20, default='IMAGE') 
    uso = models.CharField(max_length=20, choices=TIPO_USO, default='ALBUM')
    legenda = models.TextField(blank=True)
    edicoes = models.JSONField(default=dict, blank=True) 
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    class Meta: ordering = ['-criado_em']

# --- MODELOS ANTIGOS (RESTAURADOS PARA O SISTEMA FUNCIONAR) ---

class Post(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    conteudo = models.TextField(blank=True, null=True)
    imagem = models.ImageField(upload_to='posts/img/', blank=True, null=True)
    video = models.FileField(upload_to='posts/video/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_curtidos', blank=True)
    VISIBILIDADE_CHOICES = [('PUBLIC', 'Público'), ('FRIENDS', 'Amigos'), ('PRIVATE', 'Privado')]
    visibilidade = models.CharField(max_length=10, choices=VISIBILIDADE_CHOICES, default='PUBLIC')
    def __str__(self): return f"Post de {self.autor}"

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

class Grupo(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    descricao = models.TextField(blank=True)
    capa = models.ImageField(upload_to='grupos/', blank=True, null=True)
    membros = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos_participa', blank=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='grupos_admin', blank=True)
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='grupos_criados', null=True)
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    local = models.CharField(max_length=200)
    organizador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='eventos_confirmados', blank=True)

class Friendship(models.Model):
    user_from = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship_creator', on_delete=models.CASCADE)
    user_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship_receiver', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pendente'), ('ACCEPTED', 'Aceito')], default='PENDING')
    class Meta: unique_together = ('user_from', 'user_to')

class Conversa(models.Model):
    participantes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversas')
    atualizado_em = models.DateTimeField(auto_now=True)
    is_ai_chat = models.BooleanField(default=False)

class Mensagem(models.Model):
    conversa = models.ForeignKey(Conversa, on_delete=models.CASCADE, related_name='mensagens')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    texto = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications', on_delete=models.CASCADE)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='caused_notifications', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_post = models.ForeignKey('Post', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    class Meta: ordering = ['-created_at']

class Story(models.Model):
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    imagem = models.ImageField(upload_to='stories/img/', blank=True, null=True)
    video = models.FileField(upload_to='stories/video/', blank=True, null=True)
    legenda = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    expira_em = models.DateTimeField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.expira_em: self.expira_em = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

class Denuncia(models.Model):
    TIPOS = [('BULLYING', 'Bullying'), ('SPAM', 'Spam'), ('VIOLENCIA', 'Violência'), ('OUTRO', 'Outro')]
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    resolvido = models.BooleanField(default=False)