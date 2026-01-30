import os

# Caminho do arquivo de lista do feed (onde está o erro)
FEED_LIST_PATH = os.path.join('yourlife', 'social', 'templates', 'social', 'components', 'home', 'feed_list_content.html')

# Conteúdo corrigido e validado (CSS separado e limpo)
NEW_CONTENT = """{% load static %}

<div class="hidden w-full space-y-10 skeleton-wrapper">
    {% for i in "123" %}
    <div class="relative w-full aspect-[4/5] rounded-[2.5rem] bg-slate-800/50 border border-white/10 overflow-hidden">
         <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent skeleton-shimmer"></div>
    </div>
    {% endfor %}
</div>

<div class="w-full space-y-10 real-content">
    {% if posts %}
        {% for post in posts %}
            <div class="feed-item-anim" style="animation-delay: 0.{{ forloop.counter }}s;">
                {% include 'social/feed/post_card.html' with post=post %}
            </div>
        {% endfor %}
    {% else %}
        <div class="flex flex-col items-center justify-center py-32 text-center">
            <div class="relative mb-6">
                <div class="absolute inset-0 bg-indigo-500 blur-3xl opacity-20 animate-pulse"></div>
                <div class="relative flex items-center justify-center w-24 h-24 text-indigo-400 border rounded-full shadow-xl bg-slate-900 border-indigo-500/30">
                    <i class="text-4xl fa-solid fa-wind animate-bounce"></i>
                </div>
            </div>
            <h3 class="text-sm font-black tracking-[0.2em] uppercase text-slate-500">Silêncio no Horizonte</h3>
            <p class="max-w-xs mt-3 font-medium leading-relaxed text-slate-500">
                Parece que não há novas histórias por aqui.
            </p>
            <a href="{% url 'yourlife_social:explore' %}" class="mt-8 px-8 py-3 bg-indigo-600 text-white text-[10px] font-black uppercase tracking-widest rounded-2xl shadow-lg shadow-indigo-500/30 hover:bg-indigo-500 transition-all">
                Descobrir Pessoas
            </a>
        </div>
    {% endif %}
</div>

<style>
    /* Animação de Entrada dos Cards */
    .feed-item-anim {
        opacity: 0;
        transform: translateY(30px);
        animation: slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }

    @keyframes slideInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Animação do Skeleton (Brilho passando) */
    .skeleton-shimmer {
        animation: shimmer 2s infinite linear;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
</style>
"""

def fix_feed():
    try:
        # Garante que a pasta existe
        os.makedirs(os.path.dirname(FEED_LIST_PATH), exist_ok=True)
        
        # Escreve o novo conteúdo
        with open(FEED_LIST_PATH, 'w', encoding='utf-8') as f:
            f.write(NEW_CONTENT)
            
        print(f"✅ Arquivo corrigido com sucesso: {FEED_LIST_PATH}")
        print("🔄 Reinicie o servidor Django e recarregue a página (CTRL+F5).")
        
    except Exception as e:
        print(f"❌ Erro ao corrigir arquivo: {e}")

if __name__ == "__main__":
    fix_feed()