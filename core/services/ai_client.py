# niocortex/core/services/ai_client.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# URL do Micro-Serviço FastAPI (Definir no settings.py ou .env futuramente)
AI_SERVICE_URL = getattr(settings, 'AI_SERVICE_URL', 'http://localhost:8001/api/v1')

class AIClient:
    """
    Cliente para comunicação com o micro-serviço de Inteligência Artificial (FastAPI).
    """

    @staticmethod
    def _post(endpoint: str, payload: dict) -> dict:
        """ Método interno genérico para POST com tratamento de erro """
        url = f"{AI_SERVICE_URL}{endpoint}"
        try:
            # Timeout curto para não travar o Django se a IA demorar muito
            response = requests.post(url, json=payload, timeout=30) 
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            logger.error(f"Falha de conexão com Serviço de IA em {url}")
            return {"error": "Serviço de IA indisponível no momento."}
        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao chamar Serviço de IA em {url}")
            return {"error": "A IA demorou muito para responder. Tente novamente."}
        except Exception as e:
            logger.error(f"Erro genérico no AI Client: {e}")
            return {"error": f"Erro ao processar solicitação: {str(e)}"}

    @classmethod
    def analisar_aluno(cls, dados_aluno: dict) -> dict:
        """
        Envia dados do aluno para análise pedagógica.
        Payload esperado pelo FastAPI: AlunoPerformanceInput
        """
        # Mapeamento / Sanitização dos dados para o schema do FastAPI
        payload = {
            "nome_aluno": dados_aluno.get("nome", "Aluno"),
            "turma": dados_aluno.get("turma", "N/A"),
            "media_atual": float(dados_aluno.get("media", 0.0)),
            "frequencia_percentual": float(dados_aluno.get("frequencia", 0.0)),
            "historico_notas": dados_aluno.get("notas", []),
            "observacoes_recentes": dados_aluno.get("obs", [])
        }
        return cls._post("/analise/aluno", payload)

    @classmethod
    def gerar_prova(cls, tema: str, nivel: str, qtd: int = 5) -> dict:
        """
        Solicita a geração de uma prova.
        Payload esperado pelo FastAPI: GerarProvaInput
        """
        payload = {
            "tema": tema,
            "nivel_ensino": nivel,
            "quantidade_questoes": qtd,
            "tipo_questoes": "multipla_escolha", # Padrão, pode ser parametrizado
            "dificuldade": "medio"
        }
        return cls._post("/gerar/prova", payload)