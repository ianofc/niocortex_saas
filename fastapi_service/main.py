# fastapi_service/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .schemas import (
    AlunoPerformanceInput, AnalisePedagogicaOutput,
    GerarProvaInput, ProvaGeradaOutput
)
from .services.ai import gerar_analise_aluno, gerar_prova_ia
import logging

# Configuração de Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NioCortex AI Service",
    description="Micro-serviço de Inteligência Artificial para Educação",
    version="1.0.0"
)

# CORS (Permitir que o Django local acesse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "NioCortex AI"}

# --- ENDPOINTS ---

@app.post("/api/v1/analise/aluno", response_model=AnalisePedagogicaOutput)
async def analisar_aluno(payload: AlunoPerformanceInput):
    """
    Gera uma análise pedagógica completa baseada em notas e frequência.
    """
    try:
        logger.info(f"Analisando aluno: {payload.nome_aluno}")
        resultado = await gerar_analise_aluno(payload.model_dump())
        return resultado
    except Exception as e:
        logger.error(f"Erro na IA: {str(e)}")
        raise HTTPException(status_code=500, detail="Falha ao processar análise de IA.")

@app.post("/api/v1/gerar/prova", response_model=ProvaGeradaOutput)
async def gerar_prova(payload: GerarProvaInput):
    """
    Cria uma prova completa com gabarito e explicação.
    """
    try:
        logger.info(f"Gerando prova sobre: {payload.tema}")
        resultado = await gerar_prova_ia(payload.model_dump())
        return resultado
    except Exception as e:
        logger.error(f"Erro na IA: {str(e)}")
        raise HTTPException(status_code=500, detail="Falha na geração da prova.")