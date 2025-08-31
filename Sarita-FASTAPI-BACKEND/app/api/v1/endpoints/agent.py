from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app import schemas, models
from app.api import deps
import speech_recognition as sr
from pydub import AudioSegment
import io
from app.agents.corps.formacion_cultura_colonel import get_formacion_cultura_colonel_graph
from langchain_openai import ChatOpenAI
from app.core.config import settings

router = APIRouter()

# --- Agent Initialization ---
db_path = "formacion.db"
# Ensure API key is available
if not settings.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY no está configurada en el archivo .env")
llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY)
cultura_colonel_agent = get_formacion_cultura_colonel_graph(db_path, llm)

async def run_agent(prompt: str, thread_id: str, area: str):
    """Helper function to run the appropriate agent."""
    if area != "Cultura":
        return {"text": f"El agente para el área '{area}' no está disponible.", "image_url": None}

    config = {"configurable": {"thread_id": thread_id}}
    app_context = {"api": None}

    final_state = await cultura_colonel_agent.ainvoke(
        {"general_order": prompt, "app_context": app_context},
        config=config
    )
    return final_state.get("final_report", {"text": "El agente no produjo un reporte.", "image_url": None})


@router.post("/invoke-voice", response_model=schemas.AgentOutput)
async def invoke_agent_by_voice(
    *,
    db: Session = Depends(deps.get_db),
    audio_file: UploadFile = File(...),
    current_user: models.Usuario = Depends(deps.get_current_active_user),
):
    """
    Invokes the AI agent by transcribing an audio file first.
    """
    recognizer = sr.Recognizer()
    try:
        audio_data = await audio_file.read()
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_data))
        wav_data = io.BytesIO()
        audio_segment.export(wav_data, format="wav")
        wav_data.seek(0)

        with sr.AudioFile(wav_data) as source:
            audio = recognizer.record(source)

        transcribed_text = recognizer.recognize_google(audio, language="es-ES")
        print(f"Texto Transcrito: {transcribed_text}")

        # Ahora, invoca al agente con el texto transcrito
        # Usamos un thread_id basado en el user_id para la consistencia
        thread_id = f"user_{current_user.id}"
        # Asumimos un área por defecto o la extraemos de otro parámetro si estuviera disponible
        area = "Cultura"

        report = await run_agent(transcribed_text, thread_id, area)
        return report

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="No se pudo entender el audio.")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error en el servicio de reconocimiento de voz: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo de audio: {e}")


@router.post("/invoke", response_model=schemas.AgentOutput)
async def invoke_agent(
    *,
    db: Session = Depends(deps.get_db),
    agent_in: schemas.AgentInput,
    current_user: models.Usuario = Depends(deps.get_current_active_user),
):
    """
    Invokes the appropriate AI agent based on the user's area.
    """
    if agent_in.area not in ["Cultura", "Deportes"]:
        raise HTTPException(status_code=400, detail="Area must be 'Cultura' or 'Deportes'.")

    print(f"Agent invoked for thread {agent_in.thread_id} with prompt: {agent_in.prompt} in area {agent_in.area}")

    report = await run_agent(agent_in.prompt, agent_in.thread_id, agent_in.area)

    return report
