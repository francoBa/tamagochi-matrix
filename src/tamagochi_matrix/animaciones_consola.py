import os
import sys
import time
import random
from threading import Thread
from .consola import ansi


class _MatrixRain:
    """Clase interna para gestionar la animación de la lluvia digital."""

    def __init__(self, width, height, duration):
        self.width = width
        self.height = height
        self.duration = duration
        self.chars = "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプ"  # Caracteres Katakana

        # Cada columna ahora tiene una 'gota' principal y una probabilidad de tener 'chispas' secundarias
        self.columns = [
            {"y": random.randint(-height, 0), "speed": random.uniform(2, 6)}
            for _ in range(width)
        ]
        self.running = True

    def _color_gradient(self, depth):
        """Define un gradiente de color más brillante y persistente."""
        if depth == 0:
            return ansi.WHITE + ansi.BOLD  # La cabeza es blanca
        elif depth < 4:
            return ansi.GREEN_BRIGHT + ansi.BOLD  # El cuerpo cercano es brillante
        elif depth < 12:
            return ansi.GREEN_DARK  # La cola principal es verde oscuro
        else:
            return ansi.DIM + ansi.GREEN_DARK  # La cola lejana se desvanece

    def _update(self):
        start_time = time.time()

        # Creamos un 'buffer' de pantalla para dibujar sobre él
        screen = [[" " for _ in range(self.width)] for _ in range(self.height)]

        while self.running and (time.time() - start_time < self.duration):
            output = []

            # Hacemos que los caracteres existentes se desvanezcan lentamente
            for y in range(self.height):
                for x in range(self.width):
                    if (
                        screen[y][x] != " " and random.random() < 0.1
                    ):  # 10% de probabilidad de desvanecerse
                        screen[y][x] = " "
                        output.append(f"{ansi.cursor_to(y + 1, x + 1)} ")

            # Actualizamos y dibujamos las gotas principales
            for i, col in enumerate(self.columns):
                # Dibujamos la cola
                for d in range(12):
                    pos = int(col["y"]) - d
                    if 0 <= pos < self.height:
                        color = self._color_gradient(d)
                        char = random.choice(self.chars)
                        screen[pos][i] = f"{color}{char}"
                        output.append(
                            f"{ansi.cursor_to(pos + 1, i + 1)}{screen[pos][i]}"
                        )

                # Mueve la gota
                col["y"] += col["speed"] * 0.1
                if col["y"] - 12 > self.height:
                    col["y"] = random.randint(-self.height // 2, 0)
                    col["speed"] = random.uniform(2, 6)

            print("".join(output), end="", flush=True)
            time.sleep(0.04)
        self.running = False

    def run(self):
        thread = Thread(target=self._update, daemon=True)
        thread.start()
        thread.join()


def _progress_bar(task="Cargando sistema", length=30, speed=0.03):
    """Muestra una barra de progreso simple."""
    print(f"\n{ansi.GREEN_BRIGHT}{task}:{ansi.RESET}\n")
    for i in range(length + 1):
        bar = "█" * i + "-" * (length - i)
        sys.stdout.write(
            f"\r{ansi.GREEN_BRIGHT}[{bar}] {int((i/length)*100)}%{ansi.RESET}"
        )
        sys.stdout.flush()
        time.sleep(speed)
    print("\n")


def mostrar_intro_matrix():
    """Ejecuta la secuencia completa de introducción."""
    try:
        size = os.get_terminal_size()
        width, height = size.columns, size.lines
    except OSError:
        width, height = 80, 24

    try:
        print(ansi.CLEAR_SCREEN + ansi.HIDE_CURSOR, end="")

        ansi.type_text(">>> Iniciando protocolo Zion...")
        time.sleep(0.4)
        _progress_bar("Sincronizando nodos", length=35, speed=0.02)
        ansi.type_text(">>> Acceso concedido.")
        time.sleep(0.5)

        rain = _MatrixRain(width, height, duration=5)
        rain.run()

    finally:
        print(ansi.CLEAR_SCREEN + ansi.SHOW_CURSOR + ansi.RESET, end="")


def mostrar_outro_matrix():
    """Muestra una animación corta de salida."""
    try:
        size = os.get_terminal_size()
        width, height = size.columns, size.lines
    except OSError:
        width, height = 80, 24

    try:
        print(ansi.CLEAR_SCREEN + ansi.HIDE_CURSOR, end="")
        ansi.type_text(f"{ansi.YELLOW}Desconectando de la Matrix...")
        rain = _MatrixRain(width, height, duration=3)
        rain.run()
    finally:
        print(ansi.CLEAR_SCREEN + ansi.SHOW_CURSOR + ansi.RESET, end="")


# --- Bloque de Prueba y Demostración ---
if __name__ == "__main__":
    # Usamos try...except para asegurarnos de que el cursor siempre se restaure
    # si el usuario interrumpe la demo con Ctrl+C.
    try:
        # --- Prueba 1: Secuencia de Introducción Completa ---
        print("--- DEMO: Ejecutando secuencia de introducción completa ---")
        input("Presiona Enter para comenzar...")

        mostrar_intro_matrix()

        print("\nSecuencia de introducción finalizada.")
        input("\nPresiona Enter para probar la animación de salida...")

        # --- Prueba 2: Animación de Salida ---
        mostrar_outro_matrix()

        print("Demostración finalizada.\n")

    except KeyboardInterrupt:
        # Si el usuario presiona Ctrl+C, nos despedimos amablemente.
        print("\n\nDemostración interrumpida por el usuario.")
    finally:
        # Nos aseguramos de que el cursor sea visible, pase lo que pase.
        print(ansi.SHOW_CURSOR + ansi.RESET, end="")
