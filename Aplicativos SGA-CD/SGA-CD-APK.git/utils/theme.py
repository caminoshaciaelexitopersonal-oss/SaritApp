import flet as ft

# 🎨 Paleta de colores definida por el usuario
COLOR_VERDE_AZULADO = "#008F87"
COLOR_VERDE_AZULADO_BRILLANTE = "#00B3A4" # Variante para Dark Mode
COLOR_DORADO = "#FFD369"
COLOR_NEGRO_PROFUNDO = "#1C1C1E"
COLOR_BLANCO_SUAVE = "#F7F9F9"
COLOR_TEXTO_SECUNDARIO_LIGHT = "#4A4A4A"
COLOR_TEXTO_PRINCIPAL_DARK = "#EFEFEF"
COLOR_TEXTO_SECUNDARIO_DARK = "#A8A8A8"
COLOR_FONDO_TARJETA_DARK = "#2B2B2E"
COLOR_BORDE_TARJETA_LIGHT = "#E0E0E0"
COLOR_BORDE_TARJETA_DARK = "#2E5E5C"

def create_light_theme():
    """
    Crea el tema claro para la aplicación, basado en las especificaciones del usuario.
    """
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            # Fondo principal: Blanco Suave
            background=COLOR_BLANCO_SUAVE,
            # Botones primarios (acción principal): Verde-Esmeralda Azulado
            primary=COLOR_VERDE_AZULADO,
            # Barra de navegación / headers: Verde-Esmeralda Azulado
            primary_container=COLOR_VERDE_AZULADO,
            # Botones secundarios / resaltados: Dorado
            secondary=COLOR_DORADO,
            # Texto principal: Negro Profundo
            on_background=COLOR_NEGRO_PROFUNDO,
            on_surface=COLOR_NEGRO_PROFUNDO,
            # Color del texto sobre botones primarios
            on_primary=ft.colors.WHITE,
            # Tarjetas / cajas de contenido: Fondo blanco
            surface=ft.colors.WHITE,
        ),
        # Definimos colores personalizados para elementos no estándar del ColorScheme
        # para que puedan ser accedidos globalmente via page.theme.custom_colors
        custom_colors={
            "secondary_text": COLOR_TEXTO_SECUNDARIO_LIGHT,
            "card_border": COLOR_BORDE_TARJETA_LIGHT
        }
    )

def create_dark_theme():
    """
    Crea el tema oscuro para la aplicación, basado en las especificaciones del usuario.
    """
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            # Fondo principal: Negro Profundo
            background=COLOR_NEGRO_PROFUNDO,
            # Botones primarios (acción principal): Verde-Esmeralda Azulado Brillante
            primary=COLOR_VERDE_AZULADO_BRILLANTE,
            # Barra de navegación / headers: Negro con acentos
            primary_container=COLOR_NEGRO_PROFUNDO,
            # Botones secundarios / resaltados: Dorado Luminoso
            secondary=COLOR_DORADO,
            # Texto principal: Blanco Suave
            on_background=COLOR_TEXTO_PRINCIPAL_DARK,
            on_surface=COLOR_TEXTO_PRINCIPAL_DARK,
            # Color del texto sobre botones primarios
            on_primary=COLOR_NEGRO_PROFUNDO,
            # Tarjetas / cajas de contenido: Gris Oscuro
            surface=COLOR_FONDO_TARJETA_DARK,
        ),
        # Colores personalizados para el tema oscuro
        custom_colors={
            "secondary_text": COLOR_TEXTO_SECUNDARIO_DARK,
            "card_border": COLOR_BORDE_TARJETA_DARK
        }
    )
