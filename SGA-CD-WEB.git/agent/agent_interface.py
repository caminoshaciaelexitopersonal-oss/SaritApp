import asyncio
from agents.corps.formacion_cultura_colonel import get_formacion_cultura_colonel_graph
from agents.corps.formacion_deportiva_colonel import get_formacion_deportiva_colonel_graph

# This module acts as the bridge between the UI and the agent system.

async def invoke_agent_for_area(area: str, user_input: str, user_id: int, tenant_id: int) -> str:
    """
    Invokes the correct top-level agent (Colonel) based on the area context.

    Args:
        area: The area context ('Cultura' or 'Deportes').
        user_input: The natural language command from the user.
        user_id: The ID of the user invoking the agent.
        tenant_id: The ID of the tenant the user belongs to.

    Returns:
        A string containing the agent's final report.
    """
    print(f"--- 📞 Interfaz de Agente: Recibida solicitud para el área '{area}' ---")

    agent_graph = None

    # 1. Select the correct Colonel based on the area
    if area == 'Cultura':
        agent_graph = get_formacion_cultura_colonel_graph()
    elif area == 'Deportes':
        agent_graph = get_formacion_deportiva_colonel_graph()
    else:
        print(f"--- ⚠️ Interfaz de Agente: Área desconocida '{area}'. No se puede invocar al agente. ---")
        return "Error: Área de asistente no reconocida. No se puede procesar la solicitud."

    if agent_graph is None:
        return "Error: No se pudo inicializar el asistente de IA para esta área."

    # 2. Prepare the input for the agent
    # The app_context could be expanded in the future to pass more complex objects,
    # like a database connection pool or API clients.
    graph_input = {
        "general_order": user_input,
        "app_context": {
            "user_id": user_id,
            "tenant_id": tenant_id
        }
    }

    # 3. Invoke the agent and get the result
    try:
        print(f"--- 🚀 Invocando al Coronel de '{area}' con la orden: '{user_input[:50]}...' ---")
        # NOTE: Since memory (checkpointer) is disabled, we don't pass a thread_id config.
        # If memory is re-enabled, the call would look like:
        # config = {"configurable": {"thread_id": f"user_{user_id}"}}
        # final_state = await agent_graph.ainvoke(graph_input, config=config)
        final_state = await agent_graph.ainvoke(graph_input)

        report = final_state.get("final_report", "El asistente completó la tarea pero no generó un informe final.")
        print(f"--- ✅ Coronel de '{area}' completó la misión. ---")
        return report

    except Exception as e:
        print(f"--- ❌ Interfaz de Agente: Ocurrió un error crítico al invocar al Coronel de '{area}'. Error: {e} ---")
        # In a real app, you'd want more robust error logging here.
        return f"Lo siento, ocurrió un error inesperado al procesar tu solicitud. Por favor, intenta de nuevo más tarde. (Detalle: {e})"
