import os

# Definição dos caminhos
PATHS = {
    "home": "yourlife/social/templates/social/feed/home.html",
    "left_sidebar": "yourlife/social/templates/social/components/home/left_sidebar.html",
    "feed_main": "yourlife/social/templates/social/components/home/feed_main.html",
    "right_sidebar": "yourlife/social/templates/social/components/home/right_sidebar.html",
    "post_card": "yourlife/social/templates/social/feed/post_card.html",
}

# 1. HOME.HTML
# MANTIDO: bg-transparent como você exigiu.
# Ajuste: Container centralizado, scrollbars ocultas.
NEW_HOME_HTML = """{% extends 'social/layout/base_useryourlife.html' %}
{% load static %}

{% block extra_css %}
<style>
    /* Scrollbar oculta para visual limpo */
    .scrollbar-hide::-webkit-scrollbar { display: none; }
    .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
{% endblock %}

{% block content %}
<div class="min-h-screen bg-transparent">
    <div class="flex justify-center w-full mx-auto max-w-[1300px]">
        
        <aside class="sticky top-0 hidden h-screen md:flex flex-col items-end w-[80px] shrink-0 pt-6 pb-4">
            <div class="flex justify-center w-full h-full">
                {% include 'social/components/home/left_sidebar.html' %}
            </div>
        </aside>

        <main class="flex-1 max-w-[600px] w-full mx-0 md:mx-4 lg:mx-8 min-h-screen">
            <div class="w-full pb-20">
                {% include 'social/components/home/stories_bar.html' %}
                {% include 'social/components/home/feed_main.html' %}
            </div>
        </main>

        <aside class="sticky top-0 hidden h-screen lg:block w-[320px] shrink-0 pt-6 pl-2 overflow-y-auto scrollbar-hide">
            {% include 'social/components/home/right_sidebar.html' %}
        </aside>

    </div>
</div>
{% endblock %}
"""

# 2. LEFT_SIDEBAR.HTML
# Melhoria: Ícones alinhados, tooltips sutis, link de LOGOUT CORRIGIDO.
NEW_LEFT_SIDEBAR_HTML = """{% load static %}

<div class="flex flex-col items-center h-full space-y-8">
    
    <a href="{% url 'yourlife_social:home' %}" class="p-3 mb-2 transition-all rounded-full hover:bg-white/20 group backdrop-blur-sm">
        <div class="text-2xl font-black text-white transition-transform drop-shadow-md group-hover:scale-110">IO</div>
    </a>

    <nav class="flex flex-col items-center gap-6">
        
        <a href="{% url 'yourlife_social:home' %}" 
           class="relative p-3 transition-all rounded-full text-white/80 hover:text-white hover:bg-white/20 group backdrop-blur-sm"
           title="Início">
            <i class="text-2xl fas fa-home drop-shadow-sm"></i>
        </a>

        <a href="{% url 'yourlife_social:explore' %}" 
           class="p-3 transition-all rounded-full text-white/80 hover:text-white hover:bg-white/20 group backdrop-blur-sm"
           title="Explorar">
            <i class="text-2xl fas fa-hashtag drop-shadow-sm"></i>
        </a>

        <a href="{% url 'yourlife_social:groups_list' %}" 
           class="p-3 transition-all rounded-full text-white/80 hover:text-white hover:bg-white/20 group backdrop-blur-sm"
           title="Comunidades">
            <i class="text-2xl fas fa-users drop-shadow-sm"></i>
        </a>

        <a href="{% url 'yourlife_social:events_list' %}" 
           class="p-3 transition-all rounded-full text-white/80 hover:text-white hover:bg-white/20 group backdrop-blur-sm"
           title="Eventos">
            <i class="text-2xl fas fa-calendar-alt drop-shadow-sm"></i>
        </a>
        
        <div class="w-8 h-px my-1 bg-white/20"></div>

        {% if 'ALUNO' in user.role or 'PROFESSOR' in user.role %}
        <a href="{% if 'PROFESSOR' in user.role %}{% url 'lumenios:dashboard_professor' %}{% else %}{% url 'lumenios:dashboard_aluno' %}{% endif %}" 
           class="p-3 transition-all rounded-full text-white/80 hover:text-white hover:bg-white/20 group backdrop-blur-sm"
           title="Espaço Escolar">
            <i class="text-2xl fas fa-graduation-cap drop-shadow-sm"></i>
        </a>
        {% endif %}

        <a href="{% url 'yourlife_social:settings_theme' %}" 
           class="p-3 transition-all rounded-full text-white/80 hover:text-white hover:bg-white/20 group backdrop-blur-sm"
           title="Configurações">
            <i class="text-2xl fas fa-cog drop-shadow-sm"></i>
        </a>
        
        <a href="{% url 'yourlife_social:logout' %}" 
           class="p-3 transition-all rounded-full text-white/80 hover:text-red-400 hover:bg-white/20 group backdrop-blur-sm"
           title="Sair">
            <i class="text-2xl fas fa-sign-out-alt drop-shadow-sm"></i>
        </a>

    </nav>

    <div class="mt-4">
        <button onclick="document.getElementById('createPostModal').showModal()" 
                class="flex items-center justify-center w-12 h-12 text-white transition-all bg-indigo-600 border rounded-full shadow-lg hover:bg-indigo-500 hover:shadow-indigo-500/50 active:scale-95 border-white/20">
            <i class="text-xl fas fa-plus"></i>
        </button>
    </div>
    
</div>
"""

# 3. RIGHT_SIDEBAR.HTML
# Melhoria: Cards menores, visual "Glass" (vidro fosco) para integrar com o fundo transparente.
NEW_RIGHT_SIDEBAR_HTML = """{% load static %}

<div class="space-y-4 w-full max-w-[290px]">

    <a href="{% url 'core:carteirinha_digital' %}" 
       class="block w-full p-4 transition-all border shadow-sm bg-white/80 backdrop-blur-md border-white/50 rounded-2xl hover:bg-white/90 group">
        <div class="flex items-center gap-3">
            <div class="flex items-center justify-center w-10 h-10 text-indigo-600 rounded-full bg-indigo-100/80 shrink-0">
                <i class="fas fa-id-card"></i>
            </div>
            <div class="flex-1 min-w-0">
                <h3 class="text-sm font-bold truncate text-slate-800">{{ request.user.get_full_name|default:request.user.username }}</h3>
                <p class="text-[10px] text-slate-500 uppercase tracking-wide">
                    {{ request.user.role|default:"Membro" }}
                </p>
            </div>
        </div>
    </a>
    
    <div class="p-4 border shadow-sm bg-white/80 backdrop-blur-md border-white/50 rounded-2xl">
        <h2 class="flex items-center gap-2 mb-2 text-sm font-bold text-slate-800">
            <i class="text-indigo-500 fas fa-robot"></i> Talkio AI
        </h2>
        <p class="mb-3 text-xs text-slate-500">Precisa de ajuda com os estudos?</p>
        <button @click="talkioOpen = true" 
                class="w-full py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 border border-indigo-200 rounded-lg text-xs font-bold transition-colors">
            Iniciar Chat
        </button>
    </div>

    <div class="p-4 border shadow-sm bg-white/80 backdrop-blur-md border-white/50 rounded-2xl">
        <h2 class="mb-4 text-sm font-bold text-slate-800">Em Alta</h2>
        
        <div class="space-y-4">
            <a href="#" class="block cursor-pointer group">
                <div class="flex justify-between text-[10px] text-slate-500 mb-0.5">
                    <span>Tecnologia</span>
                </div>
                <div class="text-sm font-bold transition-colors text-slate-800 group-hover:text-indigo-600">#NioCortexLaunch</div>
                <div class="text-[10px] text-slate-400">12.5K posts</div>
            </a>

            <a href="#" class="block cursor-pointer group">
                <div class="flex justify-between text-[10px] text-slate-500 mb-0.5">
                    <span>Educação</span>
                </div>
                <div class="text-sm font-bold transition-colors text-slate-800 group-hover:text-indigo-600">Volta às Aulas</div>
                <div class="text-[10px] text-slate-400">5.3K posts</div>
            </a>
        </div>

        <a href="{% url 'yourlife_social:explore' %}" class="block mt-4 text-xs font-medium text-indigo-600 hover:underline">Ver tudo</a>
    </div>

</div>
"""

# 4. FEED_MAIN.HTML
# Melhoria: Header Glass real (blur). Criar post limpo. 
NEW_FEED_MAIN_HTML = """{% load static %}

<div x-data="{ feedTab: 'foryou' }" class="relative w-full">

    <div class="sticky top-0 z-20 mb-4 border-b shadow-sm backdrop-blur-xl bg-white/70 border-white/40 rounded-b-xl">
        <div class="flex w-full">
            <button @click="feedTab = 'foryou'" 
                    hx-get="{% url 'yourlife_social:home_feed_foryou' %}"
                    hx-target="#feed-content-list"
                    hx-swap="innerHTML"
                    class="relative flex-1 py-4 text-sm font-bold transition-colors"
                    :class="feedTab === 'foryou' ? 'text-slate-900' : 'text-slate-500 hover:text-slate-700'">
                Para você
                <div x-show="feedTab === 'foryou'" class="absolute bottom-0 w-12 h-1 -translate-x-1/2 bg-indigo-600 rounded-full left-1/2"></div>
            </button>
            
            <button @click="feedTab = 'following'"
                    hx-get="{% url 'yourlife_social:home_feed_following' %}"
                    hx-target="#feed-content-list"
                    hx-swap="innerHTML"
                    class="relative flex-1 py-4 text-sm font-bold transition-colors"
                    :class="feedTab === 'following' ? 'text-slate-900' : 'text-slate-500 hover:text-slate-700'">
                Seguindo
                <div x-show="feedTab === 'following'" class="absolute bottom-0 w-12 h-1 -translate-x-1/2 bg-indigo-600 rounded-full left-1/2"></div>
            </button>
        </div>
    </div>

    <div class="p-4 mb-6 border shadow-sm bg-white/80 backdrop-blur-md border-white/60 rounded-2xl">
        <div class="flex gap-3">
            <div class="shrink-0">
                 {% if request.user.avatar %}
                    <img src="{{ request.user.avatar.url }}" class="object-cover w-10 h-10 rounded-full ring-2 ring-white">
                {% else %}
                    <div class="flex items-center justify-center w-10 h-10 font-bold border border-white rounded-full bg-slate-200 text-slate-500">
                        {{ request.user.first_name|first }}
                    </div>
                {% endif %}
            </div>
            <div class="flex-1">
                <button onclick="document.getElementById('createPostModal').showModal()" 
                        class="w-full text-left py-2.5 px-4 bg-white/50 hover:bg-white text-slate-500 rounded-full text-sm border border-transparent hover:border-indigo-200 transition-all shadow-inner">
                    O que está acontecendo?!
                </button>
                <div class="flex items-center justify-between px-1 mt-3">
                    <div class="flex gap-1 text-indigo-500">
                        <button onclick="document.getElementById('createPostModal').showModal()" class="p-2 transition-colors rounded-full hover:bg-indigo-50"><i class="far fa-image"></i></button>
                        <button onclick="document.getElementById('createPostModal').showModal()" class="p-2 transition-colors rounded-full hover:bg-indigo-50"><i class="fas fa-poll-h"></i></button>
                        <button onclick="document.getElementById('createPostModal').showModal()" class="p-2 transition-colors rounded-full hover:bg-indigo-50"><i class="far fa-smile"></i></button>
                    </div>
                    <button onclick="document.getElementById('createPostModal').showModal()" class="px-5 py-1.5 bg-indigo-600 text-white font-bold rounded-full text-sm hover:bg-indigo-700 hover:shadow-lg transition-all active:scale-95">
                        Postar
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div id="feed-content-list" class="min-h-screen space-y-5">
        {% include 'social/components/home/feed_list_content.html' with posts=posts %}
    </div>
    
    <div class="flex justify-center py-10 htmx-indicator">
       <span class="loading loading-spinner loading-md text-white/80"></span>
   </div>

</div>
"""

# 5. POST_CARD.HTML
# Melhoria: Fundo Branco (para leitura) com bordas suaves. 
# CORREÇÃO CRÍTICA: Lógica de imagem (static vs media).
NEW_POST_CARD_HTML = """{% load static %}

<div class="mb-5 overflow-hidden transition-all border shadow-sm bg-white/90 backdrop-blur-sm border-white/60 rounded-2xl hover:shadow-md">
    
    <div class="flex items-start justify-between p-4">
        <div class="flex gap-3">
            <a href="{% url 'yourlife_social:profile_detail' post.autor.username %}" class="shrink-0">
                {% if post.autor.avatar %}
                    <img src="{{ post.autor.avatar.url }}" class="object-cover w-10 h-10 rounded-full ring-2 ring-white">
                {% else %}
                    <div class="flex items-center justify-center w-10 h-10 text-xs font-bold rounded-full bg-slate-100 text-slate-500">
                        {{ post.autor.first_name|first }}
                    </div>
                {% endif %}
            </a>
            <div>
                <a href="{% url 'yourlife_social:profile_detail' post.autor.username %}" class="font-bold text-slate-900 hover:text-indigo-600 transition-colors text-[15px]">
                    {{ post.autor.get_full_name|default:post.autor.username }}
                </a>
                <div class="flex items-center gap-1 text-xs text-slate-500">
                    <span>{{ post.data_criacao|timesince }} atrás</span>
                    {% if post.location %}
                        <span>• {{ post.location }}</span>
                    {% endif %}
                </div>
            </div>
        </div>
        
        {% if not post.is_system_event %}
        <button class="p-2 transition-colors rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-100">
            <i class="fas fa-ellipsis-h"></i>
        </button>
        {% endif %}
    </div>

    {% if post.conteudo %}
        <div class="px-4 pb-3">
            <p class="text-[15px] text-slate-800 whitespace-pre-wrap leading-relaxed">{{ post.conteudo }}</p>
        </div>
    {% endif %}

    {% if post.imagem %}
    <div class="w-full bg-slate-50 border-y border-slate-100">
        {% if post.is_system_event %}
            <img src="{% static post.imagem %}" class="w-full h-auto max-h-[500px] object-contain mx-auto" alt="Evento">
        {% else %}
            <img src="{{ post.imagem.url }}" class="w-full h-auto max-h-[600px] object-cover" alt="Post">
        {% endif %}
    </div>
    {% endif %}

    <div class="flex items-center justify-between px-4 py-3 border-t border-slate-100/50">
        <div class="flex gap-4">
            <button hx-post="{% url 'yourlife_social:toggle_like' post.id %}" 
                    hx-target="#like-count-{{ post.id }}"
                    class="flex items-center gap-2 transition-colors text-slate-500 hover:text-red-500 group">
                <i class="text-xl transition-transform far fa-heart group-hover:scale-110"></i>
                <span id="like-count-{{ post.id }}" class="text-sm font-medium">{{ post.total_likes }}</span>
            </button>
            
            <button class="flex items-center gap-2 transition-colors text-slate-500 hover:text-indigo-500 group">
                <i class="text-xl transition-transform far fa-comment group-hover:scale-110"></i>
                <span class="text-sm font-medium">{{ post.total_comentarios }}</span>
            </button>
        </div>
        
        <button class="transition-colors text-slate-400 hover:text-indigo-500">
            <i class="text-xl far fa-share-square"></i>
        </button>
    </div>

</div>
"""

def update_file(key, content):
    path = PATHS.get(key)
    if not path:
        return
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Atualizado: {path}")
    except Exception as e:
        print(f"❌ Erro ao atualizar {path}: {e}")

if __name__ == "__main__":
    print("🎨 Aplicando UI Transparente (Glass Clean) + Correções Técnicas...")
    update_file("home", NEW_HOME_HTML)
    update_file("left_sidebar", NEW_LEFT_SIDEBAR_HTML)
    update_file("right_sidebar", NEW_RIGHT_SIDEBAR_HTML)
    update_file("feed_main", NEW_FEED_MAIN_HTML)
    update_file("post_card", NEW_POST_CARD_HTML)
    print("🚀 Pronto! Transparência aplicada e erros corrigidos.")