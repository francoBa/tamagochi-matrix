import random
import time
import os
import sys
import importlib  # <-- Módulo para importar código dinámicamente
from pyfiglet import figlet_format
from .consola import ansi
from .animaciones_consola import mostrar_intro_matrix, mostrar_outro_matrix
from .logica_mascota import MascotaLogica
from .audio_manager import play_confirm, play_error, play_intro, play_game_over

# Importamos la clase base para poder identificar a sus hijas
from .disenios.base import MascotaDiseño
from .renderizador_consola import ConsolaRenderer
from .disenios_mascota import DisenioOriginal


def cargar_disenios_disponibles():
    """
    Explora la carpeta 'disenios', importa los módulos y encuentra todas
    las clases que heredan de MascotaDiseño.
    """
    mascotas = []
    ruta_disenios = os.path.join(os.path.dirname(__file__), "disenios")

    for nombre_archivo in os.listdir(ruta_disenios):
        if nombre_archivo.endswith(".py") and nombre_archivo not in [
            "__init__.py",
            "base.py",
        ]:
            nombre_modulo = f"tamagochi_matrix.disenios.{nombre_archivo[:-3]}"
            try:
                modulo = importlib.import_module(nombre_modulo)
                for nombre_attr in dir(modulo):
                    attr = getattr(modulo, nombre_attr)
                    if (
                        isinstance(attr, type)
                        and issubclass(attr, MascotaDiseño)
                        and attr is not MascotaDiseño
                    ):
                        mascotas.append(attr)
            except ImportError as e:
                print(
                    f"Advertencia: No se pudo cargar el diseño desde '{nombre_archivo}': {e}"
                )

    return mascotas


# --- Carga dinámica al iniciar el programa ---
MASCOTAS_DISPONIBLES = cargar_disenios_disponibles()
MASCOTAS_DISPONIBLES.append(DisenioOriginal)


class MascotaVirtual:
    """Coordina la lógica y el renderizador de la mascota."""

    def __init__(self, nombre: str):
        # El coordinador crea sus propios componentes internos
        self.logica = MascotaLogica(nombre)
        if not MASCOTAS_DISPONIBLES:
            raise RuntimeError(
                "¡Error crítico! No se encontraron diseños de mascotas para cargar."
            )
        clase_diseño_elegida = random.choice(MASCOTAS_DISPONIBLES)
        diseño = clase_diseño_elegida()
        # diseño = DisenioOriginal()
        self.renderer = ConsolaRenderer(diseño)

    ### ALINEACIÓN: El método mostrar_estado orquesta la visualización.
    def mostrar_estado(self):
        self.renderer.mostrar_estado_estatico(self.logica)

    def alimentar(self):
        """
        Gestiona la acción de alimentar, llamando a la lógica
        y mostrando el mensaje apropiado al usuario.
        """
        resultado = self.logica.alimentar()

        if resultado == "comio":
            # Aquí podríamos añadir una animación de "comer" en el futuro
            print(f"\n{ansi.GREEN}{self.logica.nombre} ha sido alimentado.{ansi.RESET}")
            play_confirm()
        elif resultado == "lleno":
            # Aquí podríamos añadir una animación de "negarse a comer"
            print(
                f"\n{ansi.YELLOW}{self.logica.nombre} está lleno y no quiere comer más.{ansi.RESET}"
            )
            # play_error()

        time.sleep(1.5)

    def jugar(self):
        if self.logica.jugar():
            print(
                f"\n{ansi.CYAN}¡Te diviertes jugando con {self.logica.nombre}!{ansi.RESET}"
            )
            play_confirm()
        else:
            print(
                f"\n{ansi.YELLOW}{self.logica.nombre} tiene mucha hambre y no puede jugar.{ansi.RESET}"
            )
            # play_error()
        time.sleep(1.5)

    def pasar_tiempo(self):
        self.logica.pasar_tiempo()

    ### MEJORA: Nueva acción con animación ###
    def accion_especial(self):
        """
        Gestiona la acción especial, consultando la lógica antes de animar.
        """
        # 1. Pregunta a la capa de lógica si la acción es posible.
        if self.logica.accion_especial():
            # 2. Si es posible, muestra el mensaje de éxito y la animación.
            print(
                f"\n{ansi.CYAN}¡{self.logica.nombre} realiza una acción especial!{ansi.RESET}\a"
            )

            # La animación se ejecuta solo si la acción fue exitosa.
            self.renderer.animar_secuencia(
                self.logica,
                secuencia_estados=["feliz", "accion1", "feliz", "accion2", "feliz"],
                delays=[0.3, 0.2, 0.2, 0.2, 0.3],
            )
            play_confirm()
        else:
            # 3. Si no es posible, muestra un mensaje informativo.
            print(
                f"\n{ansi.YELLOW}{self.logica.nombre} no tiene energía o está demasiado triste para esto.{ansi.RESET}\a"
            )
            # play_error()

        # La pausa ocurre en ambos casos.
        time.sleep(1)

    @property
    def esta_viva(self):
        return self.logica.esta_viva


# --- Punto de Entrada Principal ---
def main():
    mascota = None  # Inicializamos la variable para que exista en el 'finally'

    try:
        play_intro()
        mostrar_intro_matrix()
        titulo = figlet_format("Tamagochi Matrix", font="slant")
        print(f"\n{ansi.GREEN_BRIGHT}{titulo}{ansi.RESET}\n")

        ### TU LÓGICA DE INPUT, AHORA DENTRO DEL TRY PRINCIPAL ###
        nombre = (
            input(
                f"{ansi.BOLD}Asigna un identificador a la nueva entidad: {ansi.RESET}"
            )
            .strip()
            .title()
        )
        if not nombre:
            nombre = "Neo"

        mascota = MascotaVirtual(nombre)

        while mascota.esta_viva:
            mascota.mostrar_estado()

            opciones_menu = [
                "[1] Alimentar",
                "[2] Jugar",
                "[3] Acción Especial",
                "[4] Salir",
            ]
            menu_texto = mascota.renderer.crear_menu_enmarcado(
                "Acciones Disponibles", opciones_menu
            )
            print(menu_texto)

            opcion = input(f"{ansi.BOLD}>> {ansi.RESET}").strip()

            match opcion:
                case "1":
                    mascota.alimentar()
                case "2":
                    mascota.jugar()
                case "3":
                    mascota.accion_especial()
                case "4":
                    break
                case _:
                    print(f"\n{ansi.YELLOW}Comando no reconocido.{ansi.RESET}")
                    time.sleep(1)

            mascota.pasar_tiempo()

    except KeyboardInterrupt:
        pass

    except RuntimeError as e:
        # Atrapa el error si no se encuentran diseños
        print(
            f"\n{ansi.BACKGROUND_RED}{ansi.WHITE} ERROR DE INICIALIZACIÓN {ansi.RESET} {e}"
        )

    finally:
        print(ansi.CLEAR_SCREEN, end="")

        # Comprobamos si la mascota llegó a crearse
        if mascota and not mascota.esta_viva:
            # Si la mascota murió
            play_error()
            mascota.mostrar_estado()
            game_over_texto = figlet_format("CONEXION PERDIDA", font="small")
            print(f"\n{ansi.BACKGROUND_RED}{ansi.WHITE}{game_over_texto}{ansi.RESET}\a")
            print(f"La entidad {mascota.logica.nombre} se ha desestabilizado.")
            time.sleep(3)
        else:
            # Si el usuario salió voluntariamente (opción 4 o Ctrl+C)
            play_game_over()
            mostrar_outro_matrix()

        # Esta línea se ejecuta siempre al salir, restaurando el cursor.
        print(ansi.SHOW_CURSOR, end="")
        sys.exit(0)


if __name__ == "__main__":
    main()
