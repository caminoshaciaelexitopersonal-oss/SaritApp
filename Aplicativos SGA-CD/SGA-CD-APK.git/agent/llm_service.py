import os
import flet as ft
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_community.llms import LlamaCpp
from typing import Dict, Any, Union

# Singleton instance for the LLM
_llm_instance = None
_llm_status = "not_initialized"

def initialize_llm(page: ft.Page, config: Dict[str, Any]) -> None:
    """
    Initializes the LLM based on a dynamic configuration dictionary.
    Sets a global status that can be checked by the UI.
    Allows re-initialization if the previous attempt failed.
    """
    global _llm_instance, _llm_status
    # Allow re-initialization only if not already successfully initialized.
    if _llm_status == "initialized":
        return

    # Reset status for a new attempt
    _llm_instance = None
    _llm_status = "not_initialized"

    provider = config.get("llm_preference", "local")
    _llm_status = f"initializing_{provider}"
    print(f"--- 🧠 Inicializando LLM con proveedor: '{provider}' ---")

    llm = None
    if provider == "openai":
        api_key = config.get("openai_api_key")
        if not api_key:
            _llm_status = "error_openai_key_missing"
        else:
            llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    elif provider == "google":
        api_key = config.get("google_api_key")
        if not api_key:
            _llm_status = "error_google_key_missing"
        else:
            llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-1.5-flash")

    elif provider == "local":
        model_path = config.get("local_model_path")
        if not model_path or not os.path.exists(model_path):
            _llm_status = "error_local_model_missing"
        else:
            try:
                # n_gpu_layers=0 as we assume no GPU acceleration on mobile for now
                llm = LlamaCpp(model_path=model_path, n_ctx=2048, n_gpu_layers=0, verbose=True)
                _llm_status = "initialized"
            except Exception as e:
                _llm_status = f"error_loading_local_model: {e}"

    elif provider == "rules_based":
        # This is a placeholder for the non-AI assistant
        # We can create a dummy class that mimics the LLM interface
        class RulesBasedAssistant:
            def invoke(self, *args, **kwargs):
                return "Esta es una respuesta del asistente basado en reglas."
        llm = RulesBasedAssistant()
    else:
        _llm_status = "error_unknown_provider"

    if llm:
        _llm_instance = llm
        _llm_status = "initialized"
        print(f"--- ✅ LLM del proveedor '{provider}' inicializado correctamente. ---")

def get_llm_instance() -> Any:
    """Returns the singleton LLM instance."""
    return _llm_instance

def get_llm_status() -> str:
    """Returns the current status of the LLM initialization."""
    return _llm_status
