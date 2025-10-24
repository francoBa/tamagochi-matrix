from .consola import Style
from .logica_mascota import MascotaLogica
from .disenios_mascota import DisenioOriginal
from .renderizador_consola import ConsolaRenderer


class MascotaVirtual:
    """Coordina la lógica y el renderizador de la mascota."""

    def __init__(self, nombre: str):
        # El coordinador crea sus propios componentes internos
        self.logica = MascotaLogica(nombre)
        diseño = DisenioOriginal()
        self.renderer = ConsolaRenderer(diseño)

    ### ALINEACIÓN: El método mostrar_estado orquesta la visualización.
    def mostrar_estado(self):
        self.renderer.mostrar_estado_estatico(self.logica)

    # --- Métodos para fases futuras ---
    def alimentar(self):
        pass

    def jugar(self):
        pass


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

    # --- Objetivo de la Fase 1: Mostrar un frame y salir ---
    mascota.mostrar_estado()

    input("\nPresiona Enter para terminar...")


if __name__ == "__main__":
    main()
