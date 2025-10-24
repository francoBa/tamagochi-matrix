from .consola import Fore, Style, CLEAR_SCREEN
from .logica_mascota import MascotaLogica
from .disenios_mascota import MascotaDisenio


# Importaciones adicionales SOLO para el bloque de prueba
import time
from .disenios_mascota import DisenioOriginal  # Necesitamos un diseño real para probar


class ConsolaRenderer:
    """Gestiona toda la salida visual en la consola."""

    def __init__(self, diseño: MascotaDisenio):
        self.diseño = diseño

    def _dibujar_frame_completo(self, logica: MascotaLogica, estado_arte: str):
        print(CLEAR_SCREEN, end="")

        arte_mascota = self.diseño.get_arte(estado_arte)
        print(f"{Fore.GREEN}{arte_mascota}{Style.RESET_ALL}")

        nombre_formateado = f"{Style.BRIGHT}Mascota: {logica.nombre}{Style.NORMAL}"
        print(f"{nombre_formateado.center(40)}")
        print("-" * 40)
        print(f" Hambre: {logica.hambre}%")
        print(f" Felicidad:   {logica.felicidad}%")
        print("-" * 40)

    def mostrar_estado_estatico(self, logica: MascotaLogica):
        estado_actual = logica.get_estado_actual()
        self._dibujar_frame_completo(logica, estado_actual)


# --- Bloque de Prueba y Demostración ---
if __name__ == "__main__":
    print(f"{Style.BRIGHT}--- PRUEBAS DEL MÓDULO RENDERIZADOR ---{Style.RESET_ALL}")
    # --- PASO 1: Crear las dependencias que necesita el Renderizador ---
    # 1.1 - Necesitamos un objeto de Diseño. Usamos el que ya creamos.
    diseño_de_prueba = DisenioOriginal()
    print("Dependencia 'DiseñoOriginal' creada.")
    # 1.2 - Creamos el Renderizador, pasándole su dependencia de diseño.
    renderizador = ConsolaRenderer(diseño_de_prueba)
    print("Renderizador creado y listo para probar.\n")
    input("Presiona Enter para comenzar la demostración de renderizado...")
    # --- PASO 2: Probar el renderizado en diferentes escenarios ---
    # Escenario 1: Mascota Feliz (estado por defecto)
    print("\n--- Escenario 1: Renderizando una mascota FELIZ ---")
    mascota_feliz = MascotaLogica("Felicia")
    renderizador.mostrar_estado_estatico(mascota_feliz)
    input("\nPrueba completada. Presiona Enter para el siguiente escenario...")
    # Escenario 2: Mascota Triste
    print("\n--- Escenario 2: Renderizando una mascota TRISTE ---")
    mascota_triste = MascotaLogica("Tristón")
    mascota_triste.felicidad = 30
    renderizador.mostrar_estado_estatico(mascota_triste)
    input("\nPrueba completada. Presiona Enter para el siguiente escenario...")
    # Escenario 3: Mascota Disgustada
    print("\n--- Escenario 3: Renderizando una mascota DISGUSTADA ---")
    mascota_disgustada = MascotaLogica("Furia")
    mascota_disgustada.hambre = 80
    mascota_disgustada.felicidad = 40
    renderizador.mostrar_estado_estatico(mascota_disgustada)
    input("\nPrueba completada. Presiona Enter para finalizar...")

    print(
        f"\n{Style.BRIGHT}--- FIN DE LAS PRUEBAS DEL RENDERIZADOR ---{Style.RESET_ALL}"
    )
