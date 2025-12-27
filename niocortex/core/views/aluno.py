from django.shortcuts import render
from pedagogical.models import Aluno, Turma

def student_painel(request):
    """
    View para o painel de cursos do aluno.
    Busca as salas do aluno logado.
    """
    try:
        aluno = Aluno.objects.get(user=request.user)
        salas = aluno.turma.salas.all() if aluno.turma else []
    except Aluno.DoesNotExist:
        salas = []
    return render(request, 'lumenios/aluno/painel_cursos.html', {'salas': salas})