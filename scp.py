import os

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[NAV] {path} atualizado.")

# 1. CSS REFINADO PARA COLUNA ÚNICA E ANIMAÇÕES
talkio_css = """
:root {
    --glass-bg: rgba(255, 255, 255, 0.5);
    --glass-border: rgba(255, 255, 255, 0.3);
    --primary-blue: #2563eb;
}

.talkio-wrapper {
    height: 100vh;
    width: 100%;
    overflow: hidden;
    position: relative;
    background: transparent;
}

/* Efeito de Vidro Fosco */
.glass-effect {
    backdrop-filter: blur(25px) saturate(180%);
    -webkit-backdrop-filter: blur(25px) saturate(180%);
}

.view-pane {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.2s;
}

/* Animação estilo App Mobile */
.pane-hidden-left { transform: translateX(-100%); opacity: 0; pointer-events: none; }
.pane-hidden-right { transform: translateX(100%); opacity: 0; pointer-events: none; }
.pane-active { transform: translateX(0); opacity: 1; z-index: 10; }

.contact-pill {
    margin: 8px 16px;
    padding: 14px;
    border-radius: 24px;
    background: rgba(255, 255, 255, 0.3);
    border: 1px solid var(--glass-border);
    cursor: pointer;
    transition: all 0.2s;
}

.contact-pill:active { transform: scale(0.97); background: rgba(255, 255, 255, 0.6); }

.msg-bubble {
    max-width: 85%;
    padding: 14px 18px;
    border-radius: 22px;
    font-size: 14px;
    margin-bottom: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}

.msg-in { background: white; align-self: flex-start; border-bottom-left-radius: 4px; }
.msg-out { background: var(--primary-blue); color: white; align-self: flex-end; border-bottom-right-radius: 4px; }

.no-scrollbar::-webkit-scrollbar { display: none; }
"""

# 2. TEMPLATE TALKIO COM LÓGICA DE ALTERNÂNCIA (LISTA <-> CHAT)
talkio_index = """
{% load static %}
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{% static 'core/css/talkio_messenger.css' %}">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body class="font-sans bg-transparent text-slate-900">

<div class="talkio-wrapper" x-data="{ view: 'list', activeChat: null }">

    <div class="view-pane glass-effect" :class="view === 'list' ? 'pane-active' : 'pane-hidden-left'">
        <header class="p-6 pb-4">
            <div class="flex items-center justify-between mb-6">
                <h1 class="text-3xl font-black tracking-tighter">Talkio</h1>
                <div class="flex gap-2">
                    <button class="flex items-center justify-center w-10 h-10 border rounded-full bg-white/40 border-white/20"><i class="text-sm fas fa-edit"></i></button>
                </div>
            </div>
            <div class="relative">
                <i class="fas fa-search absolute left-4 top-3.5 text-slate-400 text-sm"></i>
                <input type="text" placeholder="Buscar conversas..." 
                       class="w-full py-3 pr-4 text-sm transition-all border outline-none pl-11 bg-white/50 border-white/20 rounded-2xl focus:bg-white">
            </div>
        </header>

        <div class="flex-1 py-2 overflow-y-auto no-scrollbar">
            <p class="px-8 text-[10px] font-black uppercase tracking-widest text-slate-400 mb-4">Conversas Recentes</p>
            
            <div class="flex items-center gap-4 contact-pill" @click="view = 'chat'; activeChat = 'Círculo Global'">
                <div class="flex items-center justify-center text-xl text-white rounded-full shadow-lg w-14 h-14 bg-gradient-to-tr from-blue-600 to-cyan-400 shadow-blue-500/20">
                    <i class="fas fa-globe-americas"></i>
                </div>
                <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-base font-black truncate">Círculo Global</span>
                        <span class="text-[10px] font-bold text-blue-500 uppercase">Agora</span>
                    </div>
                    <p class="text-sm truncate text-slate-500">Você: Fala galera, o que manda?</p>
                </div>
            </div>

            <div class="flex items-center gap-4 contact-pill" @click="view = 'chat'; activeChat = 'Ian Santos'">
                <img src="https://ui-avatars.com/api/?name=Ian+Santos&background=0D8ABC&color=fff" class="border-2 border-white rounded-full shadow-md w-14 h-14">
                <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between mb-1">
                        <span class="text-base font-bold truncate">Ian Santos</span>
                        <span class="text-[10px] text-slate-400">14:20</span>
                    </div>
                    <p class="text-sm truncate text-slate-400">O design está ficando incrível!</p>
                </div>
            </div>
        </div>
    </div>

    <div class="view-pane bg-white/20 glass-effect" :class="view === 'chat' ? 'pane-active' : 'pane-hidden-right'">
        <header class="flex items-center gap-4 p-4 px-6 border-b border-white/20 bg-white/20">
            <button @click="view = 'list'" class="flex items-center justify-center w-10 h-10 transition rounded-full text-slate-600 hover:bg-white/40">
                <i class="fas fa-chevron-left"></i>
            </button>
            <div class="flex items-center gap-3">
                <div class="flex items-center justify-center w-10 h-10 font-bold text-white bg-blue-600 rounded-full" x-text="activeChat ? activeChat[0] : ''"></div>
                <div>
                    <h3 class="text-sm font-black" x-text="activeChat"></h3>
                    <p class="text-[10px] text-green-600 font-bold uppercase">Ativo agora</p>
                </div>
            </div>
        </header>

        <div id="chat-log" class="flex flex-col flex-1 p-6 overflow-y-auto no-scrollbar">
            <div class="msg-bubble msg-in">Olá! Bem-vindo à sua conversa segura no <b>Talkio</b>.</div>
            <div class="msg-bubble msg-out">Fala! Agora a navegação está perfeita para mobile.</div>
        </div>

        <div class="p-4 border-t bg-white/30 border-white/10">
            <form id="chat-form" class="flex items-center gap-3 bg-white rounded-[2rem] p-1.5 shadow-2xl border border-white/50">
                <button type="button" class="p-3 transition text-slate-400 hover:text-blue-600"><i class="text-lg fas fa-paperclip"></i></button>
                <input type="text" id="chat-input" autocomplete="off" placeholder="Sua mensagem..." 
                       class="flex-1 px-2 py-3 text-sm bg-transparent outline-none text-slate-700">
                <button type="submit" class="flex items-center justify-center w-12 h-12 text-white bg-blue-600 rounded-full shadow-lg">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </form>
        </div>
    </div>

</div>

<script>
    // Lógica simples de log de chat (conectada ao seu Socket no futuro)
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatLog = document.getElementById('chat-log');

    chatForm.onsubmit = function(e) {
        e.preventDefault();
        const text = chatInput.value.trim();
        if(!text) return;

        const div = document.createElement('div');
        div.className = 'msg-bubble msg-out';
        div.innerText = text;
        chatLog.appendChild(div);
        chatInput.value = '';
        chatLog.scrollTop = chatLog.scrollHeight;
    };
</script>
</body>
</html>
"""

# EXECUTAR ATUALIZAÇÕES
write_file('static/core/css/talkio_messenger.css', talkio_css)
write_file('yourlife/social/templates/social/talkio/index.html', talkio_index)

print("\\n[SUCESSO] Talkio atualizado para navegação em Pilha (Mobile Style).")
print("- Lista e Chat agora alternam entre si, ocupando 100% do espaço.")
print("- Efeito Glassmorphism mantido e botão de voltar adicionado.")