import re
import flet as ft

def get_device_ram_gb(page: ft.Page) -> float | None:
    """
    Detects the total RAM of the device in Gigabytes.
    On Android, it reads /proc/meminfo.
    For other platforms (desktop), it uses psutil.
    """
    if page.platform == "android":
        try:
            with open('/proc/meminfo', 'r') as f:
                meminfo = f.read()
            match = re.search(r'MemTotal:\s+(\d+)\s+kB', meminfo)
            if match:
                total_kb = int(match.group(1))
                total_gb = total_kb / (1024 * 1024)
                print(f"--- ℹ️ RAM de Android detectada: {total_gb:.2f} GB ---")
                return total_gb
            return None
        except Exception:
            return None # Fallback if /proc/meminfo is not available or readable
    else:
        # Desktop platform (Windows, macOS, Linux)
        try:
            import psutil
            total_bytes = psutil.virtual_memory().total
            total_gb = total_bytes / (1024 ** 3)
            print(f"--- ℹ️ RAM de Escritorio detectada: {total_gb:.2f} GB ---")
            return total_gb
        except ImportError:
            print("--- ⚠️ psutil no está instalado. Devolviendo valor simulado. ---")
            return 8.0 # Fallback mock value
        except Exception as e:
            print(f"--- ❌ Error al leer la información de RAM con psutil: {e} ---")
            return None
