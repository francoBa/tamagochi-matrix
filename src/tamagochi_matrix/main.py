import random
import time
import os
import sys
import importlib  # <-- Módulo para importar código dinámicamente
from pyfiglet import figlet_format
from .consola import Style, Fore, Back
from .logica_mascota import MascotaLogica

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
            print(
                f"\n{Fore.GREEN}{self.logica.nombre} ha sido alimentado.{Style.RESET_ALL}"
            )
        elif resultado == "lleno":
            # Aquí podríamos añadir una animación de "negarse a comer"
            print(
                f"\n{Fore.YELLOW}{self.logica.nombre} está lleno y no quiere comer más.{Style.RESET_ALL}"
            )

        time.sleep(1.5)

    def jugar(self):
        if self.logica.jugar():
            print(
                f"\n{Fore.CYAN}¡Te diviertes jugando con {self.logica.nombre}!{Style.RESET_ALL}"
            )
        else:
            print(
                f"\n{Fore.YELLOW}{self.logica.nombre} tiene mucha hambre y no puede jugar.{Style.RESET_ALL}"
            )
        time.sleep(1.5)

    def pasar_tiempo(self):
        self.logica.pasar_tiempo()

    ### MEJORA: Nueva acción con animación ###
    def accion_especial(self):
        """Realiza una acción especial animada."""
        # Podríamos tener varias animaciones y elegir una al azar.
        print(
            f"\n{Fore.CYAN}¡{self.logica.nombre} está haciendo algo increíble!{Style.RESET_ALL}"
        )

        # Necesitarás generar arte para "bailar1" y "bailar2" con tu script
        # Si no existen, usará el diseño por defecto.
        self.renderer.animar_secuencia(
            self.logica,
            secuencia_estados=["feliz", "bailar1", "feliz", "bailar2", "feliz"],
            delays=[0.3, 0.2, 0.2, 0.2, 0.3],
        )
        # Las acciones especiales también pueden afectar las estadísticas
        self.logica.felicidad = min(100, self.logica.felicidad + 5)
        self.logica.hambre = min(100, self.logica.hambre + 5)

    @property
    def esta_viva(self):
        return self.logica.esta_viva


# --- Punto de Entrada Principal ---
def main():
    ### TAREA FASE 3: TÍTULO CON PYFIGLET ###
    titulo = figlet_format("Tamagochi Matrix", font="slant")
    print(f"{Fore.GREEN}{titulo}{Style.RESET_ALL}")

    nombre = input(
        f"{Style.BRIGHT}Asigna un identificador a la nueva entidad: {Style.RESET_ALL}"
    ).strip()
    if not nombre:
        nombre = "Neo"

    try:
        mascota = MascotaVirtual(nombre)
    except RuntimeError as e:
        print(f"\n{Back.RED}{Fore.WHITE} ERROR DE INICIALIZACIÓN {Style.RESET_ALL} {e}")
        return

    try:
        while mascota.esta_viva:
            mascota.mostrar_estado()

            ### TAREA FASE 3: MENÚ ENMARCADO ###
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

            try:
                opcion = input(f"{Style.BRIGHT}>> {Style.RESET_ALL}").strip()
            except KeyboardInterrupt:
                break

            match opcion:
                case "1":
                    mascota.alimentar()
                case "2":
                    mascota.jugar()
                case "3":
                    mascota.accion_especial()
                case "4":
                    print(f"\n{Fore.CYAN}Cerrando conexión...{Style.RESET_ALL}")
                    break
                case _:
                    print(f"\n{Fore.YELLOW}Comando no reconocido.{Style.RESET_ALL}")
                    time.sleep(1)

            mascota.pasar_tiempo()

    finally:
        # Limpiamos la pantalla una última vez
        print("\033c", end="")

        if not mascota.esta_viva:
            # Si la mascota murió, mostramos el estado final
            mascota.mostrar_estado()
            game_over_texto = figlet_format("CONEXION PERDIDA", font="small")
            print(f"\n{Back.RED}{Fore.WHITE}{game_over_texto}{Style.RESET_ALL}")
            print(f"La entidad {mascota.logica.nombre} se ha desestabilizado.")
        else:
            # Si el usuario salió voluntariamente
            print(
                f"\n{Fore.CYAN}Conexión terminada. ¡Hasta la próxima!{Style.RESET_ALL}\n"
            )

        # Nos aseguramos de que el cursor sea visible al salir
        print("\033[?25h", end="")
        sys.exit(0)


if __name__ == "__main__":
    main()
