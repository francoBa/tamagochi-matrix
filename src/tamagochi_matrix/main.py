import random
import time
import os
import importlib  # <-- Módulo para importar código dinámicamente
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

    @property
    def esta_viva(self):
        return self.logica.esta_viva


# --- Punto de Entrada Principal ---
def main():
    print("Iniciando Mascota Virtual...")
    nombre = input(
        f"{Style.BRIGHT}Elige un nombre para tu mascota: {Style.RESET_ALL}"
    ).strip()
    if not nombre:
        nombre = "Firulais"  # Usamos el nombre del ejercicio como defecto

    ### ALINEACIÓN: Crea una instancia de la clase MascotaVirtual.
    mascota = MascotaVirtual(nombre)

    ### FASE 2: BUCLE DE JUEGO ###
    while mascota.esta_viva:
        mascota.mostrar_estado()

        # Mostramos el menú de opciones
        print("\n¿Qué quieres hacer?")
        print("[1] Alimentar  [2] Jugar  [3] Esperar  [4] Salir")
        opcion = input(f"{Style.BRIGHT}>> {Style.RESET_ALL}").strip()

        match opcion:
            case "1":
                mascota.alimentar()
            case "2":
                mascota.jugar()
            case "4":
                print(f"\n{Fore.CYAN}¡Hasta la próxima!{Style.RESET_ALL}")
                break

        print("\nEl tiempo pasa...")
        mascota.pasar_tiempo()
        time.sleep(1)

    if not mascota.esta_viva:
        mascota.mostrar_estado()
        print(
            f"\n{Back.RED}{Fore.WHITE} FIN DEL JUEGO {Style.RESET_ALL} Oh no... {nombre} se ha ido."
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(
            f"\n\n{Fore.YELLOW}Salida exitosa del juego. Programa finalizado.{Style.RESET_ALL}"
        )
