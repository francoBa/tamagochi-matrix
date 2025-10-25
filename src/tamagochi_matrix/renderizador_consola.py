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

    ### TAREA FASE 3: BARRAS DE PROGRESO ###
    def _crear_barra_progreso(
        self, valor: int, nombre: str, ancho: int = 20, invertido: bool = False
    ) -> str:
        """
        Crea una barra de progreso con colores dinámicos.
        Si 'invertido' es True, un valor bajo es bueno (verde) y uno alto es malo (rojo).
        """
        porcentaje = valor / 100.0
        # Lógica de color normal (para Felicidad)
        if not invertido:
            if porcentaje > 0.6:
                color = Fore.GREEN
            elif porcentaje > 0.3:
                color = Fore.YELLOW
            else:
                color = Fore.RED
        # Lógica de color invertida (para Hambre)
        else:
            if porcentaje > 0.7:
                color = Fore.RED  # Hambre alta es mala
            elif porcentaje > 0.4:
                color = Fore.YELLOW
            else:
                color = Fore.GREEN  # Hambre baja es buena

        relleno = int(porcentaje * ancho)
        barra = "█" * relleno + "░" * (ancho - relleno)
        return f" {Style.BRIGHT}{nombre.ljust(9)}:{Style.NORMAL} {color}[{barra}]{Style.RESET_ALL} {valor}%"

    ### TAREA FASE 3: MENÚS ENMARCADOS ###
    def crear_menu_enmarcado(self, titulo: str, opciones: list, ancho: int = 40) -> str:
        linea_borde = "╔" + "═" * (ancho - 2) + "╗"
        linea_vacia = "║" + " " * (ancho - 2) + "║"
        menu = [linea_borde, "║" + titulo.center(ancho - 2) + "║", linea_vacia]
        for opcion in opciones:
            menu.append("║" + (" " * 3 + opcion).ljust(ancho - 2) + "║")
        menu.extend([linea_vacia, "╚" + "═" * (ancho - 2) + "╝"])
        return "\n".join(menu)

    def _dibujar_frame_completo(self, logica: MascotaLogica, info_estado: dict):
        print(CLEAR_SCREEN, end="")

        arte_mascota = self.diseño.get_arte(info_estado["clave"])
        print(f"{Fore.GREEN}{arte_mascota}{Style.RESET_ALL}")

        nombre_formateado = f"{Style.BRIGHT}Mascota: {logica.nombre}{Style.NORMAL}"
        print(f"{nombre_formateado.center(40)}")

        print("-" * 40)
        print(self._crear_barra_progreso(logica.hambre, "Hambre", invertido=True))
        print(
            self._crear_barra_progreso(logica.felicidad, "Felicidad")
        )  # Felicidad usa la lógica normal

        print(f" Estado: {Style.BRIGHT}{info_estado['texto']}{Style.NORMAL}")
        print(f" {Fore.CYAN}Recomendación: {info_estado['hint']}{Style.RESET_ALL}")
        print("-" * 40)

    def mostrar_estado_estatico(self, logica: MascotaLogica):
        # Ahora obtenemos el diccionario de información completo
        info_estado = logica.get_info_estado()
        self._dibujar_frame_completo(logica, info_estado)

    ### MEJORA: Función de animación genérica ###
    def animar_secuencia(
        self, logica: MascotaLogica, secuencia_estados: list, delays: list
    ):
        for i, estado_arte in enumerate(secuencia_estados):
            # Obtenemos la info del estado actual para el texto, pero usamos
            # el estado de la secuencia para el arte.
            info_actual = logica.get_info_estado()
            self._dibujar_frame_completo(
                logica,
                {
                    "clave": estado_arte,
                    "texto": info_actual["texto"],
                    "hint": info_actual["hint"],
                },
            )
            time.sleep(delays[i])


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
