# niocortex/core/services/ai_client.py

import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# URL do Micro-Serviço FastAPI (IO CONSCIOS)
AI_SERVICE_URL = getattr(settings, 'AI_SERVICE_URL', 'http://localhost:8000')

class AIClient:
    """
    Cliente para comunicação com o micro-serviço de Inteligência Artificial (FastAPI).
    Centraliza chamadas HTTP, log de erros e tratamento de exceções.
    """

    @staticmethod
    def _request(method: str, endpoint: str, payload: dict = None) -> dict:
        """ 
        Wrapper central para comunicação com o Brain.
        Gerencia Headers, Autenticação e Tratamento de Erros.
        """
        # Garante URL limpa. 
        # Nota: O endpoint deve começar com '/' (ex: '/v1/chat/interact')
        base = AI_SERVICE_URL.rstrip('/')
        path = endpoint.lstrip('/')
        url = f"{base}/{path}"
        
        headers = {
            "X-Service-Token": getattr(settings, 'SERVICE_TOKEN_SECRET', 'dev-secret'),
            "Content-Type": "application/json"
        }

        try:
            # Timeout ajustado: 60s para POST (geração) e 45s para GET
            timeout = 60 if method == 'POST' else 45

            if method == 'GET':
                response = requests.get(url, params=payload, headers=headers, timeout=timeout)
            else:
                response = requests.post(url, json=payload, headers=headers, timeout=timeout)
            
            response.raise_for_status()
            return response.json()

        except requests.exceptions.ConnectionError:
            logger.critical(f"IO CONSCIUS OFFLINE: Falha ao conectar em {url}")
            return {"error": "O Cérebro (IO Conscios) não está respondendo. Verifique se o container está rodando."}
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao chamar Serviço de IA em {url}")
            return {"error": "A IA demorou muito para responder. Tente novamente."}
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição para IA: {e}")
            # Tenta extrair mensagem de erro detalhada da API FastAPI
            msg = "Erro desconhecido na comunicação com a IA."
            if e.response is not None:
                try:
                    detail = e.response.json().get('detail')
                    if detail:
                        msg = f"Erro da IA: {detail}"
                except:
                    pass
            return {"error": msg}
        
        except Exception as e:
            logger.error(f"Erro genérico no AIClient: {e}")
            return {"error": f"Erro interno de processamento: {str(e)}"}

    @classmethod
    def check_proactive_thought(cls, user, current_path: str, meta_data: dict = {}) -> dict:
        """
        Pergunta ao Conscios: "Vendo onde estou, você tem algo a dizer?"
        """
        role = "GUEST"
        if user.is_superuser: role = "ADMIN"
        elif hasattr(user, 'professor'): role = "PROFESSOR"
        elif hasattr(user, 'aluno'): role = "ALUNO"
        
        payload = {
            "user_role": role,
            "current_page": current_path,
            "user_name": user.first_name,
            "meta_data": meta_data
        }
        
        return cls._request('POST', 'proactive/observe', payload)
    
    @classmethod
    def _post(cls, endpoint: str, payload: dict) -> dict:
        """ Atalho para requisições POST """
        return cls._request('POST', endpoint, payload)

    # ------------------------------------------------------------------
    # ANALYTICS (DADOS)
    # ------------------------------------------------------------------

    @classmethod
    def analisar_aluno(cls, dados_aluno: dict) -> dict:
        """
        Envia dados do aluno para análise pedagógica e risco de evasão.
        """
        payload = {
            "nome_aluno": dados_aluno.get("nome", "Aluno"),
            "turma": dados_aluno.get("turma", "N/A"),
            "media_atual": float(dados_aluno.get("media", 0.0) or 0.0),
            "frequencia_percentual": float(dados_aluno.get("frequencia", 0.0) or 0.0),
            "historico_notas": dados_aluno.get("notas", []),
            "observacoes_recentes": dados_aluno.get("obs", [])
        }
        # Endpoint ajustado para o padrão v1
        return cls._post("/v1/education/analyze_student", payload)

    # ------------------------------------------------------------------
    # GERAÇÃO DE CONTEÚDO (COPILOTO PEDAGÓGICO)
    # ------------------------------------------------------------------

    @classmethod
    def gerar_prova(cls, dados_prova: dict) -> dict:
        """
        Solicita a geração de uma prova completa (Avaliação Formal).
        """
        payload = {
            "tema": dados_prova.get("tema", "Assunto Geral"),
            "nivel": dados_prova.get("nivel_ensino", "Ensino Fundamental"),
            "quantidade_questoes": int(dados_prova.get("qtd_questoes", 5)),
            "tipo_questoes": dados_prova.get("tipo_questoes", ["Múltipla Escolha"]), 
            "dificuldade": dados_prova.get("dificuldade", "Médio"),
            "instrucoes_extras": dados_prova.get("instrucoes_extras", "")
        }
        return cls._post("/v1/education/exam", payload)

    @classmethod
    def gerar_plano_aula(cls, dados_plano: dict) -> dict:
        """
        Gera um roteiro de aula alinhado à BNCC.
        """
        payload = {
            "tema": dados_plano.get("tema"),
            "disciplina": dados_plano.get("disciplina", "Geral"),
            "nivel": dados_plano.get("ano_turma", "Geral"), 
            "duracao": dados_plano.get("duracao", "50 minutos"),
            "metodologia": dados_plano.get("metodologia", "Ativa")
        }
        return cls._post("/v1/education/lesson_plan", payload)

    @classmethod
    def gerar_atividade(cls, dados_atividade: dict) -> dict:
        """
        Gera exercícios de fixação ou dinâmicas lúdicas.
        """
        payload = {
            "tema": dados_atividade.get("tema"),
            "nivel": dados_atividade.get("nivel"),
            "ludico": dados_atividade.get("ludico", False)
        }
        return cls._post("/v1/education/activity", payload)

    # ------------------------------------------------------------------
    # MÓDULO ALMA (INTERAÇÃO & OBSERVADOR)
    # ------------------------------------------------------------------

    @classmethod
    def chat_universal(cls, mensagem: str, usuario_user) -> dict:
        """
        Envia mensagem para o Conscios com o contexto total do usuário logado.
        Define o 'Role' (Papel) para que a IA responda com a persona correta.
        """
        role = "GUEST"
        contexto = {}
        
        # Lógica para determinar o Papel do usuário no sistema
        if usuario_user.is_superuser:
            role = "ADMIN"
        elif hasattr(usuario_user, 'professor'): # Verifica relacionamento reverso
            role = "PROFESSOR"
            contexto['nome_professor'] = usuario_user.first_name
        elif hasattr(usuario_user, 'aluno'):
            role = "ALUNO"
            contexto['turma'] = "Turma Padrão" 
        elif hasattr(usuario_user, 'responsavel'):
            role = "RESPONSAVEL"
            
        payload = {
            "message": mensagem,
            "role": role,
            "user_name": usuario_user.first_name or usuario_user.username,
            "context": contexto
        }
        
        return cls._post("/v1/chat/interact", payload)

    @classmethod
    def check_proactive_thought(cls, user, current_path: str, meta_data: dict = {}) -> dict:
        """
        Pergunta ao Conscios: "Vendo onde estou, você tem algo a dizer?"
        Usado para o widget de sugestões proativas (Balãozinho).
        """
        role = "GUEST"
        if user.is_superuser: 
            role = "ADMIN"
        elif hasattr(user, 'professor'):
            role = "PROFESSOR"
        elif hasattr(user, 'aluno'):
            role = "ALUNO"
        
        payload = {
            "user_role": role,
            "current_page": current_path,
            "user_name": user.first_name or user.username,
            "meta_data": meta_data
        }
        
        return cls._post("/v1/proactive/observe", payload)
    
    # ------------------------------------------------------------------
    # MÓDULO JUIZ (SEGURANÇA)
    # ------------------------------------------------------------------

    @classmethod
    def moderar_conteudo(cls, texto: str, contexto: str = "escolar") -> dict:
        """ 
        O Juiz verifica se um texto (chat, obs) é seguro.
        Retorna: { "seguro": bool, "motivo": str, "tags": [] }
        """
        payload = {
            "content": texto,
            "context": contexto
        }
        return cls._post("/v1/judge/evaluate", payload)