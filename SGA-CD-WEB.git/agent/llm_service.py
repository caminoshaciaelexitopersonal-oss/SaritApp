import json
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

_llm_instance = None
_config = None

def _load_config():
    """Loads the configuration from config.json, assuming it's in the CWD."""
    global _config
    if _config is None:
        config_path = 'config.json'
        try:
            with open(config_path, 'r') as f:
                _config = json.load(f)
        except FileNotFoundError:
            print(f"--- 🚨 CRITICAL ERROR: config.json not found in the current directory. ---")
            print(f"--- CWD: {os.getcwd()} ---")
            # Fallback to a default or raise an exception
            raise
    return _config

def get_llm():
    """
    Initializes and returns a singleton LLM instance based on the configuration file.
    """
    global _llm_instance
    if _llm_instance is not None:
        return _llm_instance

    config = _load_config()
    provider = config.get("llm_provider", "openai")
    provider_config = config.get("providers", {}).get(provider, {})

    print(f"--- 🧠 Initializing LLM instance for provider: {provider} ---")

    if provider == "openai":
        api_key = provider_config.get("api_key")
        if not api_key or "YOUR-OPENAI-API-KEY-HERE" in api_key:
            print("--- ⚠️ WARNING: OpenAI API key is not configured in config.json ---")
            # Langchain will try to use environment variable OPENAI_API_KEY
            api_key = None

        _llm_instance = ChatOpenAI(
            model=provider_config.get("model", "gpt-4o"),
            temperature=0,
            model_kwargs={"response_format": {"type": "json_object"}},
            api_key=api_key
        )
    elif provider == "google":
        api_key = provider_config.get("api_key")
        if not api_key or "YOUR-GOOGLE-API-KEY-HERE" in api_key:
            print("--- ⚠️ WARNING: Google API key is not configured in config.json ---")
            # Langchain will try to use environment variable GOOGLE_API_KEY
            api_key = None

        _llm_instance = ChatGoogleGenerativeAI(
            model=provider_config.get("model", "gemini-1.5-flash"),
            google_api_key=api_key,
            # Google's JSON mode is handled differently, often via specific model versions
            # or parameters within the invoke call. We assume the model supports it.
        )
    elif provider == "ollama":
        _llm_instance = ChatOllama(
            base_url=provider_config.get("base_url", "http://localhost:11434"),
            model=provider_config.get("model", "llama3"),
            temperature=provider_config.get("temperature", 0),
            # Ollama supports JSON mode via a format parameter
            format="json"
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    return _llm_instance
