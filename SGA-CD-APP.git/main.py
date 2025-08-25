import flet as ft
import sqlite3
import os

# --- App-specific Imports ---
from utils.theme import create_light_theme, create_dark_theme
from utils.i18n_service import Translator
from agent.llm_service import initialize_llm, get_llm_status
from utils.database_manager import initialize_local_database
# --- View Imports ---
from views.login import login_view
from views.shared.dashboard_view import dashboard_view
# ... (import other views as needed, this is a simplified example)
from views.jefe_area.jefe_area_principal import jefe_area_principal_view
from views.profesor_principal import profesor_principal
from views.admin_principal import admin_principal
# ... etc.

def check_llm_status(page: ft.Page):
    """
    Checks the LLM status and shows an alert dialog if there's a dependency issue.
    """
    status = get_llm_status()

    if status == "error_ollama_not_found":
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Ollama no encontrado"),
            content=ft.Column([
                ft.Text("Para usar la IA en modo local en su escritorio, necesita tener Ollama instalado y en ejecución."),
                ft.Markdown("Puede descargarlo desde [el sitio web oficial de Ollama](https://ollama.com)."),
            ]),
            actions=[ft.TextButton("Entendido", on_click=lambda _: page.close(dlg))],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    elif status == "error_local_model_missing":
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Fichero de Modelo no Encontrado"),
            content=ft.Text("El fichero del modelo de IA local no fue encontrado. La aplicación debe ser reinstalada desde una fuente completa."),
            actions=[ft.TextButton("Entendido", on_click=lambda _: page.close(dlg))],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

def main(page: ft.Page):
    # --- Inicialización de Servicios Críticos ---
    initialize_local_database(page)

    # La inicialización del LLM ahora requiere la configuración del inquilino,
    # que se obtendría después del login. Por ahora, usamos una config por defecto.
    # TODO: Mover la inicialización del LLM para después del login.
    default_config = {"llm_preference": "local"}
    initialize_llm(page, default_config)

    # Comprobar el estado del LLM y mostrar alertas si es necesario.
    check_llm_status(page)

    page.title = "SGA-CD: Sistema de Gestión Académica"

    # --- Theme Setup ---
    page.theme = create_light_theme()
    page.dark_theme = create_dark_theme()
    # Start in light mode by default, or get from session if previously set
    page.theme_mode = page.session.get("theme_mode") or ft.ThemeMode.LIGHT

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        # Save the preference in the session
        page.session.set("theme_mode", page.theme_mode)
        page.update()

    theme_switcher_button = ft.IconButton(
        icon=ft.icons.BRIGHTNESS_4_OUTLINED,
        tooltip="Cambiar tema",
        on_click=toggle_theme,
    )

    # --- Internationalization Service ---
    user_lang = page.session.get("user_lang") or "es"
    translator = Translator(initial_lang=user_lang)
    page.translator = translator

    # --- OAuth (simplified for brevity) ---
    # ... (OAuth provider setup would go here)

    # --- Main Router Logic ---
    def route_change(route):
        page.views.clear()
        user_id = page.session.get("user_id")

        # --- Public Routes ---
        if page.route == "/" or page.route == "/login":
            page.views.append(login_view(page, None, None)) # Providers not needed for this example
        # ... other public routes

        # --- Protected Routes ---
        elif user_id is None:
            page.go("/login")
        else:
            user_role = page.session.get("user_role")
            tenant_id = page.session.get("tenant_id")

            def add_view(view_function, **kwargs):
                # This helper now consistently adds the theme switcher to all views
                view = view_function(page=page, user_id=user_id, tenant_id=tenant_id, **kwargs)
                if hasattr(view, 'appbar') and view.appbar:
                    # Ensure actions list exists
                    if not hasattr(view.appbar, 'actions'):
                        view.appbar.actions = []
                    # Add theme switcher if not already present
                    if not any(isinstance(c, ft.IconButton) and c.tooltip == "Cambiar tema" for c in view.appbar.actions):
                        view.appbar.actions.append(theme_switcher_button)
                page.views.append(view)

            # Simplified Routing Table
            # In the real file, this would be the large if/elif block
            routing_table = {
                "/dashboard": (dashboard_view, ["alumno", "profesor", "admin_empresa", "jefe_area"]),
                "/admin_home": (admin_principal, ["admin_empresa"]),
                "/jefe_area/home": (jefe_area_principal_view, ["jefe_area"]),
                "/profesor_home": (profesor_principal, ["profesor"])
                # ... add all other routes and their allowed roles here
            }

            route_found = False
            for route_path, (view_func, allowed_roles) in routing_table.items():
                if page.route == route_path:
                    if user_role in allowed_roles:
                        add_view(view_func)
                        route_found = True
                        break

            if not route_found:
                # Fallback for any other route or unauthorized access
                page.go('/dashboard')

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route if page.route else "/")

if __name__ == "__main__":
    # The database is now initialized by running `init_db.py` separately.
    ft.app(target=main, assets_dir="assets")
