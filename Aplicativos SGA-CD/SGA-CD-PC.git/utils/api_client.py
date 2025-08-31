import requests
import json
from typing import List, Dict, Any

class ApiClient:
    """
    Cliente para interactuar con el backend API del sistema SGA-CD.
    Este actúa como el "Gestor de Datos" para la aplicación Flet.
    """
    def __init__(self, base_url: str, tenant_api_key: str):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": tenant_api_key
        }

    def _make_request(self, method: str, endpoint: str, headers: Dict = None, **kwargs) -> Dict | List | None:
        """Método de ayuda para realizar peticiones a la API."""
        url = f"{self.base_url}{endpoint}"

        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)

        try:
            response = requests.request(method, url, headers=request_headers, **kwargs)
            response.raise_for_status()

            # Manejar respuestas sin contenido
            if response.status_code == 204:
                return {}

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error de API en '{method} {endpoint}': {e}")
            return None
        except json.JSONDecodeError:
            print(f"Error de decodificación JSON en '{method} {endpoint}'")
            return None

    # --- Métodos de API ---

    def get_user_context(self, user_id: int) -> Dict | None:
        """Obtiene el contexto de un usuario desde el backend."""
        headers = {"X-USER-ID": str(user_id)}
        return self._make_request("GET", "/api/user_context", headers=headers)

    def get_clases_profesor(self, profesor_id: int) -> List[Dict] | None:
        """Obtiene la lista de clases para un profesor específico."""
        params = {"profesor_id": profesor_id}
        return self._make_request("GET", "/api/clases", params=params)

    def create_alumno(self, alumno_data: Dict) -> Dict | None:
        """Crea un nuevo alumno."""
        return self._make_request("POST", "/api/alumnos", json=alumno_data)

    def get_llm_config(self) -> Dict | None:
        """Obtiene la configuración de LLM del inquilino desde el servidor."""
        return self._make_request("GET", "/api/config/llm")

    def set_llm_config(self, config_data: Dict) -> bool:
        """Guarda la configuración de LLM del inquilino en el servidor."""
        response = self._make_request("POST", "/api/config/llm", json=config_data)
        return response is not None and response.get("status") == "success"

    def pull_sync_data(self, last_sync_timestamp: str = None) -> Dict | None:
        """Obtiene los cambios del servidor para la sincronización."""
        params = {}
        if last_sync_timestamp:
            params['last_sync_timestamp'] = last_sync_timestamp
        return self._make_request("GET", "/api/sync/pull", params=params)

    def push_sync_data(self, data_batch: Dict) -> bool:
        """Envía los cambios locales al servidor para la sincronización."""
        response = self._make_request("POST", "/api/sync/push", json=data_batch)
        return response is not None and response.get("status") == "success"
