import os
from threading import Thread
from typing import Callable


def _playsound_fallback(path: str, block: bool = True):
    """Función de reemplazo que no hace nada si 'playsound' no está instalado."""
    pass


# Intentamos importar la función real. Si falla, usamos nuestra función falsa.
try:
    from playsound import playsound as _playsound_real

    PLAYSOUND_AVAILABLE = True
    # Asignamos la función real a nuestra variable de trabajo
    _playsound_func: Callable = _playsound_real
except ImportError:
    PLAYSOUND_AVAILABLE = False
    # Asignamos la función falsa a nuestra variable de trabajo
    _playsound_func: Callable = _playsound_fallback


# Obtenemos la ruta a la carpeta de assets, sin importar desde dónde se ejecute el script.
_ASSETS_PATH = os.path.join(os.path.dirname(__file__), "../../assets/sounds")


def _play_sound(filename: str):
    """Función interna para reproducir un sonido en un hilo separado."""
    if not PLAYSOUND_AVAILABLE:
        # Si la librería no está, usamos el bip del sistema como fallback.
        print("\a", end="", flush=True)
        return

    path = os.path.join(_ASSETS_PATH, filename)
    if os.path.exists(path):
        # Ejecutamos el sonido en un hilo para que no bloquee el juego.
        thread = Thread(target=_playsound_func, args=(path,), daemon=True)
        thread.start()
    else:
        # Si el archivo de sonido no se encuentra, usamos el bip del sistema.
        print("\a", end="", flush=True)


# --- Funciones públicas que usaremos en el juego ---
def play_confirm():
    """Sonido para una acción exitosa."""
    _play_sound("confirm.mp3")


def play_error():
    """Sonido para una acción fallida o un error."""
    _play_sound("error.mp3")


def play_intro():
    """Sonido de bienvenida al juego."""
    _play_sound("intro.mp3")


def play_game_over():
    """Sonido para el fin del juego."""
    _play_sound("game_over.mp3")
