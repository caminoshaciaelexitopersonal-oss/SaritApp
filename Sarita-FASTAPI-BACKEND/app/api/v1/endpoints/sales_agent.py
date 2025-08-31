from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api import deps
from app.agents.corps.ventas_colonel import get_sales_agent_executor
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class SalesAgentInput(BaseModel):
    query: str
    # En el futuro, podríamos añadir un session_id para mantener el historial
    # session_id: str | None = None

class SalesAgentOutput(BaseModel):
    reply: str

@router.post("")
async def invoke_sales_agent(
    agent_in: SalesAgentInput,
    db: Session = Depends(deps.get_db)
) -> SalesAgentOutput:
    """
    Public endpoint to interact with the AI Sales Agent.
    This endpoint now uses a dynamically configured agent.
    """
    if not agent_in.query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La consulta (query) no puede estar vacía."
        )

    logger.info(f"Invocando al Agente de Ventas con la consulta: '{agent_in.query}'")

    try:
        # For a public endpoint, we assume a default tenant (e.g., the main company)
        inquilino_id = 1
        agent_executor = get_sales_agent_executor(db=db, inquilino_id=inquilino_id)

        response_text = await agent_executor.ainvoke({"question": agent_in.query})
        logger.info(f"Respuesta generada por el agente: '{response_text}'")
        return SalesAgentOutput(reply=response_text)
    except Exception as e:
        logger.error(f"Error al invocar el agente de ventas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error al procesar su solicitud."
        )
