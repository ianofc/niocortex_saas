import os

print("🔥 INICIANDO SUPER SCRIPT DE CORREÇÃO UI/UX - YOURLIFE...")

# ==============================================================================
# 1. MAPEAMENTO DE ARQUIVOS
# ==============================================================================
BASE_DIR = "yourlife/social/templates/social"

FILES_TO_WRITE = {
    # 1. HOME: O container principal (Fundo Transparente)
    f"{BASE_DIR}/feed/home.html": """{% extends 'social/layout/base_useryourlife.html' %}
{% load static %}

{% block extra_css %}
<style>
    /* Ocultar scrollbar mantendo funcionalidade */
    .scrollbar-hide::-webkit-scrollbar { display: none; }
    .scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
{% endblock %}

{% block content %}
<div class="min-h-screen bg-transparent">
    
    <div class="flex justify-center w-full mx-auto max-w-[1300px]">
        
        <aside class="sticky top-0 hidden h-screen md:flex flex-col items-end w-[80px] lg:w-[250px] shrink-0 pt-6 pb-4 pr-2">
            <div class="w-full h-full">
                {% include 'social/components/home/left_sidebar.html' %}
            </div>
        </aside>

        <main class="flex-1 max-w-[600px] w-full mx-0 md:mx-4 lg:mx-8 min-h-screen pb-20">
            {% include 'social/components/home/stories_bar.html' %}
            {% include 'social/components/home/feed_main.html' %}
        </main>

        <aside class="sticky top-0 hidden h-screen lg:block w-[320px] shrink-0 pt-6 pl-2 overflow-y-auto scrollbar-hide">
            {% include 'social/components/home/right_sidebar.html' %}
        </aside>

    </div>
</div>
{% endblock %}
""",

    # 2. LEFT SIDEBAR: Navegação Limpa (Com correção do Logout)
    f"{BASE_DIR}/components/home/left_sidebar.html": """{% load static %}

<div class="flex flex-col items-center h-full px-2 space-y-6 lg:items-start">
    
    <a href="{% url 'yourlife_social:home' %}" class="p-3 mb-2 transition-colors rounded-full hover:bg-white/10 group">
        <div class="text-3xl font-black text-indigo-600 transition-transform drop-shadow-sm group-hover:scale-105">
            IO
        </div>
    </a>

    <nav class="flex flex-col w-full gap-2">
        
        <a href="{% url 'yourlife_social:home' %}" 
           class="flex items-center gap-4 p-3 transition-all rounded-full hover:bg-white/60 group backdrop-blur-sm">
            <i class="text-2xl fas fa-home text-slate-800 group-hover:text-indigo-600"></i>
            <span class="hidden text-xl font-bold lg:block text-slate-800">Início</span>
        </a>

        <a href="{% url 'yourlife_social:explore' %}" 
           class="flex items-center gap-4 p-3 transition-all rounded-full hover:bg-white/60 group backdrop-blur-sm">
            <i class="text-2xl fas fa-hashtag text-slate-800 group-hover:text-indigo-600"></i>
            <span class="hidden text-xl font-medium lg:block text-slate-800">Explorar</span>
        </a>

        <a href="{% url 'yourlife_social:groups_list' %}" 
           class="flex items-center gap-4 p-3 transition-all rounded-full hover:bg-white/60 group backdrop-blur-sm">
            <i class="text-2xl fas fa-users text-slate-800 group-hover:text-indigo-600"></i>
            <span class="hidden text-xl font-medium lg:block text-slate-800">Comunidades</span>
        </a>

        <a href="{% url 'yourlife_social:events_list' %}" 
           class="flex items-center gap-4 p-3 transition-all rounded-full hover:bg-white/60 group backdrop-blur-sm">
            <i class="text-2xl far fa-calendar-alt text-slate-800 group-hover:text-indigo-600"></i>
            <span class="hidden text-xl font-medium lg:block text-slate-800">Eventos</span>
        </a>

        {% if 'ALUNO' in user.role or 'PROFESSOR' in user.role %}
        <a href="{% if 'PROFESSOR' in user.role %}{% url 'lumenios:dashboard_professor' %}{% else %}{% url 'lumenios:dashboard_aluno' %}{% endif %}" 
           class="flex items-center gap-4 p-3 mt-2 transition-all rounded-full hover:bg-blue-50/80 group backdrop-blur-sm">
            <i class="text-2xl fas fa-graduation-cap text-slate-800 group-hover:text-blue-600"></i>
            <span class="hidden text-xl font-medium lg:block text-slate-800">Escola</span>
        </a>
        {% endif %}

        <a href="{% url 'yourlife_social:settings_theme' %}" 
           class="flex items-center gap-4 p-3 transition-all rounded-full hover:bg-white/60 group backdrop-blur-sm">
            <i class="text-2xl fas fa-cog text-slate-800 group-hover:text-indigo-600"></i>
            <span class="hidden text-xl font-medium lg:block text-slate-800">Ajustes</span>
        </a>

        <a href="{% url 'yourlife_social:logout' %}" 
           class="flex items-center gap-4 p-3 mt-4 transition-all rounded-full hover:bg-red-50/80 group backdrop-blur-sm">
            <i class="text-2xl fas fa-sign-out-alt text-slate-800 group-hover:text-red-600"></i>
            <span class="hidden text-xl font-medium lg:block text-slate-800 group-hover:text-red-600">Sair</span>
        </a>

    </nav>

    <div class="flex justify-center w-full mt-8 lg:justify-start">
        <button onclick="document.getElementById('createPostModal').showModal()" 
                class="w-14 h-14 lg:w-[90%] lg:h-12 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all flex items-center justify-center active:scale-95">
            <i class="text-xl fas fa-feather-alt lg:hidden"></i>
            <span class="hidden text-lg font-bold lg:inline">Publicar</span>
        </button>
    </div>

</div>
""",

    # 3. FEED MAIN: Header Glass e Feed Limpo
    f"{BASE_DIR}/components/home/feed_main.html": """{% load static %}

<div x-data="{ feedTab: 'foryou' }" class="relative w-full">

    <div class="sticky top-0 z-20 mb-4 border-b backdrop-blur-md bg-white/70 border-white/50 rounded-b-xl">
        <div class="flex w-full">
            <button @click="feedTab = 'foryou'" 
                    hx-get="{% url 'yourlife_social:home_feed_foryou' %}"
                    hx-target="#feed-content-list"
                    hx-swap="innerHTML"
                    class="flex-1 py-4 text-[15px] font-bold transition-colors relative"
                    :class="feedTab === 'foryou' ? 'text-slate-900' : 'text-slate-500 hover:bg-white/40'">
                Para você
                <div x-show="feedTab === 'foryou'" class="absolute bottom-0 w-12 h-1 -translate-x-1/2 bg-indigo-600 rounded-full left-1/2"></div>
            </button>
            
            <button @click="feedTab = 'following'"
                    hx-get="{% url 'yourlife_social:home_feed_following' %}"
                    hx-target="#feed-content-list"
                    hx-swap="innerHTML"
                    class="flex-1 py-4 text-[15px] font-bold transition-colors relative"
                    :class="feedTab === 'following' ? 'text-slate-900' : 'text-slate-500 hover:bg-white/40'">
                Seguindo
                <div x-show="feedTab === 'following'" class="absolute bottom-0 w-12 h-1 -translate-x-1/2 bg-indigo-600 rounded-full left-1/2"></div>
            </button>
        </div>
    </div>

    <div class="p-4 mb-6 border shadow-sm bg-white/80 backdrop-blur-sm border-white/60 rounded-2xl">
        <div class="flex gap-3">
            <div class="shrink-0">
                 {% if request.user.avatar %}
                    <img src="{{ request.user.avatar.url }}" class="object-cover w-10 h-10 rounded-full ring-2 ring-white">
                {% else %}
                    <div class="flex items-center justify-center w-10 h-10 text-sm font-bold text-indigo-600 bg-indigo-100 rounded-full">
                        {{ request.user.first_name|first }}
                    </div>
                {% endif %}
            </div>
            <div class="flex-1">
                <button onclick="document.getElementById('createPostModal').showModal()" 
                        class="w-full text-left py-2.5 px-4 bg-slate-100/80 hover:bg-white text-slate-500 rounded-full text-sm border border-transparent hover:border-indigo-200 transition-all cursor-text shadow-inner">
                    O que está acontecendo?!
                </button>
                <div class="flex items-center justify-between px-1 mt-3">
                    <div class="flex gap-2 text-indigo-500">
                        <button onclick="document.getElementById('createPostModal').showModal()" class="p-2 transition-colors rounded-full hover:bg-indigo-50" title="Imagem"><i class="far fa-image"></i></button>
                        <button onclick="document.getElementById('createPostModal').showModal()" class="p-2 transition-colors rounded-full hover:bg-indigo-50" title="Vídeo"><i class="fas fa-video"></i></button>
                        <button onclick="document.getElementById('createPostModal').showModal()" class="p-2 transition-colors rounded-full hover:bg-indigo-50" title="Emoji"><i class="far fa-smile"></i></button>
                    </div>
                    <button onclick="document.getElementById('createPostModal').showModal()" class="px-5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-full text-sm shadow-md transition-all active:scale-95">
                        Postar
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div id="feed-content-list" class="space-y-4">
        {% include 'social/components/home/feed_list_content.html' with posts=posts %}
    </div>
    
    <div class="flex justify-center py-10 htmx-indicator">
       <span class="text-indigo-600 loading loading-spinner loading-md"></span>
   </div>

</div>
""",

    # 4. POST CARD: Lógica de Imagem Corrigida e Visual Limpo
    f"{BASE_DIR}/feed/post_card.html": """{% load static %}

<div class="mb-4 overflow-hidden transition-shadow duration-200 bg-white border border-gray-100 shadow-sm rounded-2xl hover:shadow-md">
    
    <div class="flex items-start justify-between p-4">
        <div class="flex gap-3">
            <a href="{% url 'yourlife_social:profile_detail' post.autor.username %}" class="shrink-0 group">
                {% if post.autor.avatar %}
                    <img src="{{ post.autor.avatar.url }}" class="object-cover w-10 h-10 transition-all rounded-full ring-2 ring-transparent group-hover:ring-indigo-100">
                {% else %}
                    <div class="flex items-center justify-center w-10 h-10 text-xs font-bold rounded-full bg-slate-200 text-slate-500">
                        {{ post.autor.first_name|first }}
                    </div>
                {% endif %}
            </a>
            
            <div class="flex flex-col">
                <a href="{% url 'yourlife_social:profile_detail' post.autor.username %}" class="font-bold text-slate-900 hover:underline text-[15px] leading-tight">
                    {{ post.autor.get_full_name|default:post.autor.username }}
                </a>
                <div class="flex items-center gap-1 text-xs text-slate-500">
                    <span>@{{ post.autor.username }}</span>
                    <span>·</span>
                    <span>{{ post.data_criacao|timesince }}</span>
                </div>
            </div>
        </div>
        
        {% if not post.is_system_event %}
        <button class="p-2 transition-colors rounded-full text-slate-400 hover:text-indigo-600 hover:bg-indigo-50">
            <i class="fas fa-ellipsis-h"></i>
        </button>
        {% endif %}
    </div>

    {% if post.conteudo %}
        <div class="px-4 pb-3">
            <p class="text-[15px] text-slate-900 whitespace-pre-line leading-relaxed">{{ post.conteudo }}</p>
        </div>
    {% endif %}

    {% if post.imagem %}
    <div class="w-full mt-1 bg-slate-50 border-y border-slate-100">
        {% if post.is_system_event %}
            <img src="{% static post.imagem %}" class="w-full h-auto max-h-[550px] object-contain mx-auto" alt="Imagem do Sistema">
        {% else %}
            <img src="{{ post.imagem.url }}" class="w-full h-auto max-h-[550px] object-cover" alt="Foto do Post">
        {% endif %}
    </div>
    {% endif %}

    <div class="flex items-center justify-between px-4 py-3 text-slate-500">
        
        <button hx-post="{% url 'yourlife_social:toggle_like' post.id %}" 
                hx-target="#like-cnt-{{ post.id }}"
                class="flex items-center gap-2 transition-colors group hover:text-pink-600">
            <div class="p-2 transition-colors rounded-full group-hover:bg-pink-50">
                <i class="text-lg far fa-heart"></i>
            </div>
            <span id="like-cnt-{{ post.id }}" class="text-xs font-bold">{{ post.total_likes|default:"0" }}</span>
        </button>
        
        <button class="flex items-center gap-2 transition-colors group hover:text-blue-500">
            <div class="p-2 transition-colors rounded-full group-hover:bg-blue-50">
                <i class="text-lg far fa-comment"></i>
            </div>
            <span class="text-xs font-bold">{{ post.total_comentarios|default:"0" }}</span>
        </button>
        
        <button class="flex items-center gap-2 transition-colors group hover:text-green-500">
            <div class="p-2 transition-colors rounded-full group-hover:bg-green-50">
                <i class="text-lg far fa-share-square"></i>
            </div>
        </button>
        
    </div>

</div>
""",

    # 5. RIGHT SIDEBAR: Minimalista, Clean, Glass
    f"{BASE_DIR}/components/home/right_sidebar.html": """{% load static %}

<div class="space-y-6 w-full max-w-[300px]">

    <div class="relative group">
        <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
            <i class="fas fa-search text-slate-400 group-focus-within:text-indigo-600"></i>
        </div>
        <input type="text" 
               class="block w-full py-3 pr-4 leading-5 transition-shadow bg-white border rounded-full shadow-sm pl-11 border-slate-200 placeholder-slate-400 focus:outline-none focus:bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" 
               placeholder="Buscar no YourLife">
    </div>

    <div class="p-4 border shadow-sm bg-white/80 backdrop-blur-md border-white/60 rounded-2xl">
        <h3 class="mb-3 text-sm font-bold text-slate-800">Identidade</h3>
        <div class="flex items-center gap-3">
            <div class="flex items-center justify-center w-10 h-10 text-indigo-600 bg-indigo-100 rounded-xl">
                <i class="fas fa-qrcode"></i>
            </div>
            <div>
                <p class="text-sm font-bold text-slate-900">{{ request.user.first_name }}</p>
                <p class="text-[10px] text-slate-500 uppercase font-bold">{{ request.user.role }}</p>
            </div>
        </div>
        <a href="{% url 'core:carteirinha_digital' %}" class="block w-full py-2 mt-3 text-xs font-bold text-center transition-colors rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700">
            Ver Carteirinha
        </a>
    </div>

    <div class="p-4 border shadow-sm bg-white/80 backdrop-blur-md border-white/60 rounded-2xl">
        <h3 class="mb-4 text-lg font-black text-slate-800">O que está acontecendo</h3>
        
        <div class="space-y-4">
            <a href="#" class="block group">
                <div class="flex justify-between text-[11px] text-slate-500 mb-0.5">
                    <span>Tecnologia · Ao vivo</span>
                </div>
                <div class="text-sm font-bold text-slate-900 group-hover:text-indigo-600">Lançamento NioCortex</div>
                <div class="text-[11px] text-slate-500">12.4K posts</div>
            </a>

            <a href="#" class="block group">
                <div class="flex justify-between text-[11px] text-slate-500 mb-0.5">
                    <span>Educação · Brasil</span>
                </div>
                <div class="text-sm font-bold text-slate-900 group-hover:text-indigo-600">Volta às Aulas 2026</div>
                <div class="text-[11px] text-slate-500">50K posts</div>
            </a>
        </div>
        
        <a href="#" class="block mt-4 text-sm font-medium text-indigo-600 hover:text-indigo-700">Mostrar mais</a>
    </div>

    <div class="flex flex-wrap gap-x-3 gap-y-1 text-[11px] text-slate-400 px-2">
        <a href="#" class="hover:underline">Termos de Serviço</a>
        <a href="#" class="hover:underline">Política de Privacidade</a>
        <a href="#" class="hover:underline">Acessibilidade</a>
        <span>© 2026 NioCortex</span>
    </div>

</div>
"""
}

# ==============================================================================
# 2. EXECUÇÃO DA ESCRITA
# ==============================================================================

def write_file(filepath, content):
    # Cria o diretório se não existir
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"📁 Diretório criado: {directory}")
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Arquivo atualizado com sucesso: {filepath}")
    except Exception as e:
        print(f"❌ Erro ao escrever {filepath}: {e}")

if __name__ == "__main__":
    for path, code in FILES_TO_WRITE.items():
        write_file(path, code)
    
    print("\n🎉 SUPER SCRIPT CONCLUÍDO!")
    print("👉 Fundo home.html definido como 'bg-transparent'.")
    print("👉 Link de Logout corrigido para '{% url 'yourlife_social:logout' %}'")
    print("👉 Lógica de Imagem no Post Card corrigida (Static/Media).")
    print("👉 UI/UX limpa, minimalista e focada no conteúdo.")
    print("⚠️ Recarregue a página (Ctrl+F5) para ver as alterações.")