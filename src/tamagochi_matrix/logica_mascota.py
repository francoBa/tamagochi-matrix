import random


class MascotaLogica:
    """Gestiona los datos y reglas del juego, alineado con los requisitos originales."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.hambre = 50
        self.felicidad = 51
        self.esta_viva = True

    def get_info_estado(self) -> dict:
        """
        Devuelve un diccionario con el estado clave, el texto descriptivo
        y una recomendación para el jugador.
        """
        if not self.esta_viva:
            return {
                "clave": "muerto",
                "texto": "Desconectado",
                "hint": "No se puede hacer nada.",
            }

        if self.hambre >= 70 and self.felicidad <= 50:
            return {
                "clave": "disgustado",
                "texto": "Crítico y Triste",
                "hint": "¡Necesita comida urgentemente!",
            }

        if self.hambre >= 70:
            return {
                "clave": "disgustado",
                "texto": "Hambre Crítica",
                "hint": "Deberías alimentarlo.",
            }

        if self.felicidad <= 50:
            return {
                "clave": "triste",
                "texto": "Triste",
                "hint": "Juega con él para animarlo.",
            }

        return {
            "clave": "feliz",
            "texto": "Estable y Contento",
            "hint": "Todo va bien. ¡Sigue así!",
        }

    def get_estado_actual(self) -> str:
        """
        Determina el estado actual como una cadena de texto simple.
        ### ALINEACIÓN: Lógica de mostrar_estado.
        """
        return self.get_info_estado()["clave"]

    def alimentar(self) -> str:
        """
        Aplica la lógica de alimentar a la mascota según los requisitos.
        Devuelve un string indicando el resultado de la acción.
        """
        if self.hambre == 0:
            return "lleno"

        self.hambre -= random.randint(10, 15)
        if self.hambre < 0:
            self.hambre = 0

        # La felicidad disminuye solo si come.
        self.felicidad -= random.randint(5, 10)
        if self.felicidad < 0:
            self.felicidad = 0

        return "comio"

    def jugar(self) -> bool:
        """
        Aplica la lógica de jugar con la mascota.
        Devuelve True si pudo jugar, False si tenía demasiada hambre.
        """
        if self.hambre > 70:
            return False

        self.felicidad += random.randint(10, 25)
        if self.felicidad > 100:
            self.felicidad = 100

        self.hambre += random.randint(10, 15)
        if self.hambre > 100:
            self.hambre = 100

        return True

    def pasar_tiempo(self):
        """Simula el paso del tiempo, deteriorando las estadísticas."""
        self.hambre = min(100, self.hambre + random.randint(1, 3))
        self.felicidad = max(0, self.felicidad - random.randint(1, 2))

        if self.hambre == 100 or self.felicidad == 0:
            self.esta_viva = False


# --- Bloque de Prueba y Demostración ---
if __name__ == "__main__":
    print("--- PRUEBAS DEL MÓDULO DE LÓGICA ---")
    # Creamos una mascota de prueba
    mascota_de_prueba = MascotaLogica("Testy")
    print(f"Mascota creada: {mascota_de_prueba.nombre}\n")

    def probar_estado(descripcion, hambre, felicidad, esta_viva, estado_esperado):
        """Función auxiliar para hacer las pruebas más limpias."""
        print(f"--- Escenario: {descripcion} ---")
        # Manipulamos los atributos directamente para la prueba
        mascota_de_prueba.hambre = hambre
        mascota_de_prueba.felicidad = felicidad
        mascota_de_prueba.esta_viva = esta_viva

        estado_obtenido = mascota_de_prueba.get_estado_actual()

        print(f"Valores: Hambre={hambre}, Felicidad={felicidad}, Viva={esta_viva}")
        print(f"Estado esperado: '{estado_esperado}'")
        print(f"Estado obtenido:   '{estado_obtenido}'")

        if estado_obtenido == estado_esperado:
            print("Resultado: \033[92mPASÓ\033[0m\n")
        else:
            print("Resultado: \033[91mFALLÓ\033[0m\n")

    # --- Escenarios de prueba ---
    probar_estado("Feliz (estado inicial)", 50, 51, True, "feliz")
    probar_estado("Triste (felicidad baja)", 50, 50, True, "triste")
    probar_estado("Disgustado (hambre alta)", 70, 60, True, "disgustado")
    probar_estado(
        "Disgustado (hambre alta y felicidad baja)", 80, 40, True, "disgustado"
    )
    probar_estado("Muerto", 90, 90, False, "muerto")

    print("--- FIN DE LAS PRUEBAS ---")
