# import os
from threading import Thread

# from typing import Callable
from importlib import resources


# def _playsound_fallback(path: str, block: bool = True):
#     """Función de reemplazo que no hace nada si 'playsound' no está instalado."""
#     pass


try:
    from playsound import playsound as _playsound_real

    PLAYSOUND_AVAILABLE = True
    # _playsound_func: Callable = _playsound_real
except ImportError:
    PLAYSOUND_AVAILABLE = False
    # _playsound_func: Callable = _playsound_fallback

# sin importar dónde esté instalado.
_ASSETS_REF = resources.files("tamagochi_matrix") / "assets" / "sounds"


def _safe_play_sound(path: str):
    """
    Función envoltorio que llama a la función real de playsound
    y captura la excepción específica que esperamos en entornos headless y sin sonido.
    """
    try:
        _playsound_real(path, block=False)
    except NotImplementedError:
        pass


def _play_sound(filename: str):
    """Función interna para reproducir un sonido empaquetado."""
    if not PLAYSOUND_AVAILABLE:
        # Si la librería no está, usamos el bip del sistema como fallback.
        print("\a", end="", flush=True)
        return

    try:
        # Usamos el 'context manager' para obtener una ruta de archivo utilizable
        with resources.as_file(_ASSETS_REF / filename) as path:
            # Creamos el hilo usando nuestra variable _playsound_func a prueba de linters
            thread = Thread(
                # target=_playsound_func,
                target=_safe_play_sound,
                args=(str(path),),
                # kwargs={"block": False},
                daemon=True,
            )
            thread.start()
    except FileNotFoundError:
        # Este error se lanza si el archivo (ej. "confirm.mp3") no existe
        # dentro de la carpeta de assets del paquete.
        print(
            f"Advertencia: No se encontró el asset de sonido empaquetado '{filename}'."
        )
        print("\a", end="", flush=True)


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
