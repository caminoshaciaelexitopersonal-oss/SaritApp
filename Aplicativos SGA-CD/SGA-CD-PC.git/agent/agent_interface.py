import asyncio
import flet as ft
from agents.corps.formacion_cultura_colonel import get_formacion_cultura_colonel_graph
from agents.corps.formacion_deportiva_colonel import get_formacion_deportiva_colonel_graph
from utils.database_manager import get_db_path
from agent.llm_service import get_llm_instance

async def invoke_agent_for_area(page: ft.Page, area: str, user_input: str, user_id: int, tenant_id: int) -> str:
    """
    Invokes the correct top-level agent (Colonel) based on the area context.
    This is the main orchestration function. It uses the globally initialized LLM.
    """
    print(f"--- 📞 Interfaz de Agente: Recibida solicitud para el área '{area}' ---")

    # 1. Obtener la instancia de LLM global, que fue configurada en el flujo de setup.
    llm = get_llm_instance()
    if not llm:
        # Esto no debería ocurrir si el flujo de setup es correcto.
        return "Error Crítico: El modelo de lenguaje (LLM) no ha sido inicializado."

    # 2. Obtener la ruta a la base de datos local del usuario para la memoria del agente
    db_path = get_db_path(page)

    # 3. Seleccionar y compilar el grafo del agente correcto, pasando el LLM y la DB path
    agent_graph = None
    if area == 'Cultura':
        agent_graph = get_formacion_cultura_colonel_graph(db_path, llm)
    elif area == 'Deportes':
        # Asumiendo que formacion_deportiva_colonel sigue el mismo patrón de refactorización.
        # TODO: Refactorizar formacion_deportiva_colonel.py
        agent_graph = get_formacion_deportiva_colonel_graph(db_path, llm)
    else:
        return "Error: Área de asistente no reconocida."

    if agent_graph is None:
        return "Error: No se pudo construir el grafo del asistente de IA."

    # 4. Preparar el input y la configuración para la invocación
    # TODO: El app_context ahora necesita el ApiClient, que ya no se instancia aquí.
    # Por ahora, se pasa un contexto simplificado.
    graph_input = {"general_order": user_input, "app_context": {"user_id": user_id, "tenant_id": tenant_id, "api": None}}
    config = {"configurable": {"thread_id": f"user_{user_id}"}}

    # 5. Invocar al agente
    try:
        print(f"--- 🚀 Invocando al Coronel de '{area}' con la orden: '{user_input[:50]}...' ---")
        final_state = await agent_graph.ainvoke(graph_input, config=config)
        report = final_state['messages'][-1].content if final_state.get('messages') else "El asistente completó la tarea pero no generó un informe final."
        print(f"--- ✅ Coronel de '{area}' completó la misión. ---")
        return report
    except Exception as e:
        print(f"--- ❌ Interfaz de Agente: Ocurrió un error crítico al invocar al Coronel. Error: {e} ---")
        return f"Lo siento, ocurrió un error inesperado al procesar tu solicitud. (Detalle: {e})"
