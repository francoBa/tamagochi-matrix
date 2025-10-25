"""
consola.py
----------
Módulo auxiliar para salida en consola con colores y estilos.
"""

import random
import time
import sys


class Ansi:
    """Clase para manejar colores, estilos y control de la terminal usando códigos ANSI."""

    # --- Estilos y Control ---
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CLEAR_SCREEN = "\033[H\033[2J"  # Mueve el cursor a 1,1 y luego limpia
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

    # --- Colores True Color (temática Matrix) ---
    GREEN_BRIGHT = "\033[38;2;0;255;70m"
    GREEN_DARK = "\033[38;2;0;150;50m"
    WHITE = "\033[38;2;200;255;200m"

    # --- Colores de la Interfaz del Juego (los que ya usábamos) ---
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    CYAN = "\033[36m"
    BACKGROUND_RED = "\033[41m"

    @staticmethod
    def cursor_to(row: int, col: int) -> str:
        """Mueve el cursor a una fila y columna específicas."""
        return f"\033[{row};{col}H"

    @staticmethod
    def type_text(text: str, delay: float = 0.04):
        """Imprime texto con un efecto de máquina de escribir."""
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay + random.uniform(-0.01, 0.01))
        print()


# Instancia global para un acceso fácil
ansi = Ansi()
