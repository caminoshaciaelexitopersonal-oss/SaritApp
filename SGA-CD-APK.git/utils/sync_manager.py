import flet as ft
from .api_client import ApiClient
from .database_manager import get_db_connection

class SyncManager:
    """
    El "Motor de Datos". Gestiona la sincronización entre la base de datos
    local del cliente y la base de datos central a través de la API.
    """
    def __init__(self, page: ft.Page, api_client: ApiClient):
        self.page = page
        self.api_client = api_client

    def _detect_local_changes(self) -> dict:
        """
        Detecta los registros que han sido creados o modificados localmente
        desde la última sincronización.

        NOTA: Esta es una implementación de ejemplo muy simplificada. Un sistema
        real necesitaría un mecanismo robusto para el seguimiento de cambios,
        como tablas de 'log', timestamps de 'última modificación' en cada fila,
        o un sistema de versionado.
        """
        print("Detectando cambios locales para el 'push'...")
        # Lógica de ejemplo: obtener los 5 alumnos más recientes.
        conn = get_db_connection(self.page)
        alumnos = conn.execute("SELECT * FROM alumnos ORDER BY id DESC LIMIT 5").fetchall()
        conn.close()

        if alumnos:
            return {"alumnos": [dict(row) for row in alumnos]}
        return {}

    def _apply_server_changes(self, server_data: dict):
        """
        Aplica los datos recibidos del servidor a la base de datos local.

        NOTA: Esta es una implementación simplificada. Un sistema real necesitaría
        manejar conflictos (qué pasa si el usuario modificó el mismo registro
        localmente que también fue modificado en el servidor).
        """
        print("Aplicando cambios del servidor a la base de datos local...")
        data = server_data.get("data", {})
        conn = get_db_connection(self.page)
        cursor = conn.cursor()

        try:
            if 'clases' in data:
                for clase in data['clases']:
                    # Usar INSERT OR REPLACE para una estrategia simple de 'última escritura gana'
                    # Se necesitarían todos los campos aquí
                    cursor.execute("INSERT OR REPLACE INTO clases (id, nombre_clase, ...) VALUES (?, ?, ...)",
                                   (clase['id'], clase['nombre_clase']))

            # ... Repetir para todas las demás tablas (alumnos, etc.) ...

            conn.commit()
            print("Cambios del servidor aplicados con éxito.")
        except Exception as e:
            print(f"Error al aplicar cambios del servidor: {e}")
            conn.rollback()
        finally:
            conn.close()

    def sync_with_server(self, last_sync_timestamp: str = None) -> bool:
        """
        Ejecuta el ciclo completo de sincronización: push y luego pull.
        """
        print("--- Iniciando ciclo de sincronización ---")

        # 1. Push: Enviar cambios locales al servidor
        local_changes = self._detect_local_changes()
        if local_changes:
            print(f"Enviando {len(local_changes.get('alumnos',[]))} cambios locales al servidor...")
            push_success = self.api_client.push_sync_data(local_changes)
            if not push_success:
                print("Error: El 'push' de la sincronización falló. Abortando.")
                self.page.snack_bar = ft.SnackBar(ft.Text("Error al enviar cambios al servidor."), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()
                return False
            print("Push completado con éxito.")
        else:
            print("No se encontraron cambios locales para enviar.")

        # 2. Pull: Obtener cambios del servidor
        print("Obteniendo cambios desde el servidor...")
        server_response = self.api_client.pull_sync_data(last_sync_timestamp)
        if server_response and server_response.get("data"):
            self._apply_server_changes(server_response)
            # TODO: Guardar el nuevo `timestamp` de la sincronización en las preferencias locales.
            new_timestamp = server_response.get("timestamp")
            print(f"Pull completado. Nuevo timestamp de sincronización: {new_timestamp}")
        elif server_response:
            print("No hay nuevos datos para obtener del servidor.")
        else:
            print("Error: El 'pull' de la sincronización falló.")
            self.page.snack_bar = ft.SnackBar(ft.Text("Error al recibir datos del servidor."), bgcolor="red")
            self.page.snack_bar.open = True
            self.page.update()
            return False

        print("--- Ciclo de sincronización completado ---")
        self.page.snack_bar = ft.SnackBar(ft.Text("¡Sincronización completada!"), bgcolor="green")
        self.page.snack_bar.open = True
        self.page.update()
        return True
