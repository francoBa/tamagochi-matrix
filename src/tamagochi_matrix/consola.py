"""
consola.py
----------
Módulo auxiliar para salida en consola con colores y estilos.
Funciona con o sin 'colorama' instalado.
"""

try:
    from colorama import just_fix_windows_console, Fore, Back, Style

    just_fix_windows_console()  # Corrige colores en Windows antiguos
except ImportError:
    # === Fallback manual con secuencias ANSI ===
    class _ANSI:
        """Base para definir códigos ANSI de colores."""

        def __init__(self, mapping):
            self._map = mapping

        def __getattr__(self, name):
            return self._map.get(name, "")

    Fore = _ANSI(
        {
            "BLACK": "\033[30m",
            "RED": "\033[31m",
            "GREEN": "\033[32m",
            "YELLOW": "\033[33m",
            "BLUE": "\033[34m",
            "MAGENTA": "\033[35m",
            "CYAN": "\033[36m",
            "WHITE": "\033[37m",
            "RESET": "\033[39m",
            "LIGHTBLACK_EX": "\033[90m",
            "LIGHTRED_EX": "\033[91m",
            "LIGHTGREEN_EX": "\033[92m",
            "LIGHTYELLOW_EX": "\033[93m",
            "LIGHTBLUE_EX": "\033[94m",
            "LIGHTMAGENTA_EX": "\033[95m",
            "LIGHTCYAN_EX": "\033[96m",
            "LIGHTWHITE_EX": "\033[97m",
        }
    )

    Back = _ANSI(
        {
            "BLACK": "\033[40m",
            "RED": "\033[41m",
            "GREEN": "\033[42m",
            "YELLOW": "\033[43m",
            "BLUE": "\033[44m",
            "MAGENTA": "\033[45m",
            "CYAN": "\033[46m",
            "WHITE": "\033[47m",
            "RESET": "\033[49m",
            "LIGHTBLACK_EX": "\033[100m",
            "LIGHTRED_EX": "\033[101m",
            "LIGHTGREEN_EX": "\033[102m",
            "LIGHTYELLOW_EX": "\033[103m",
            "LIGHTBLUE_EX": "\033[104m",
            "LIGHTMAGENTA_EX": "\033[105m",
            "LIGHTCYAN_EX": "\033[106m",
            "LIGHTWHITE_EX": "\033[107m",
        }
    )

    Style = _ANSI(
        {
            "DIM": "\033[2m",
            "NORMAL": "\033[22m",
            "BRIGHT": "\033[1m",
            "RESET_ALL": "\033[0m",
        }
    )

# === Secuencias básicas ===
CLEAR_SCREEN = "\033c"
