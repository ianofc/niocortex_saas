import os

def fix_groups_view():
    print("🔧 Consertando yourlife/social/views/groups.py...")
    path = os.path.join("yourlife", "social", "views", "groups.py")
    
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("from django.shortcuts import render\nfrom django.contrib.auth.decorators import login_required\n")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "def groups_list" not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n\n@login_required\ndef groups_list(request):\n    return render(request, 'social/groups/list.html')\n")
        print("   ✅ View 'groups_list' criada.")

def fix_events_view():
    print("🔧 Consertando yourlife/social/views/events.py...")
    path = os.path.join("yourlife", "social", "views", "events.py")
    
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write("from django.shortcuts import render\nfrom django.contrib.auth.decorators import login_required\n")

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "def events_list" not in content:
        with open(path, "a", encoding="utf-8") as f:
            f.write("\n\n@login_required\ndef events_list(request):\n    return render(request, 'social/events/list.html')\n")
        print("   ✅ View 'events_list' criada.")

def fix_urls():
    print("🔧 Atualizando yourlife/social/urls.py...")
    path = os.path.join("yourlife", "social", "urls.py")
    
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verifica se as rotas já existem para não duplicar
    has_groups = "name='groups_list'" in content
    has_events = "name='events_list'" in content

    if has_groups and has_events:
        print("   ✅ Rotas já parecem estar lá. (Verifique se salvou o arquivo)")
        return

    # Se não tiver, vamos reescrever o bloco final para garantir
    # Esta abordagem é bruta mas resolve o problema de "onde inserir"
    if "urlpatterns = [" in content:
        new_routes = ""
        if not has_groups:
            new_routes += "    path('groups/', groups.groups_list, name='groups_list'),\n"
        if not has_events:
            new_routes += "    path('events/', events.events_list, name='events_list'),\n"
        
        if new_routes:
            # Insere antes do fechamento da lista
            content = content.rstrip().rstrip("]") + "\n" + new_routes + "]"
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("   ✅ Rotas de Grupos e Eventos registradas.")

if __name__ == "__main__":
    fix_groups_view()
    fix_events_view()
    fix_urls()
    print("\n🚀 CORREÇÃO APLICADA. Reinicie o servidor: python manage.py runserver")