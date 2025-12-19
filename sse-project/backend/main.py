import asyncio
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from datetime import datetime

# Configuração de logs para monitorar as conexões
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SSE Precision Backend")

# CORS necessário para comunicação entre portas diferentes (8000 -> 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def event_generator(request: Request):
    """
    Gerador de eventos que mantém a conexão viva.
    """
    try:
        while True:
            # Verifica se o cliente ainda está conectado
            if await request.is_disconnected():
                logger.info("Cliente desconectado.")
                break

            # Simulando carga de dados (ex: cotação de moedas ou sensores)
            now = datetime.now().strftime("%H:%M:%S")
            data = {
                "message": "Atualização do sistema",
                "timestamp": now,
                "status": "online"
            }

            yield {
                "event": "message", # Nome do evento que o React ouvirá
                "data": f"{data['timestamp']} - {data['message']}"
            }

            await asyncio.sleep(3)  # Intervalo de 3 segundos
    except asyncio.CancelledError:
        logger.info("Conexão cancelada para o cliente.")

@app.get("/stream")
async def stream_events(request: Request):
    return EventSourceResponse(event_generator(request))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)