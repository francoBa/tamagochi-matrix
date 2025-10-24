import random


class MascotaLogica:
    """Gestiona los datos y reglas del juego, alineado con los requisitos originales."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self.hambre = 50
        self.felicidad = 51
        self.esta_viva = True

    def get_estado_actual(self) -> str:
        """
        Determina el estado actual como una cadena de texto simple.
        ### ALINEACIÓN: Lógica de mostrar_estado.
        """
        if not self.esta_viva:
            return "muerto"

        if self.hambre >= 70 and self.felicidad <= 50:
            return "disgustado"
        if self.hambre >= 70:
            return "disgustado"
        if self.felicidad <= 50:
            return "triste"

        return "feliz"

    def alimentar(self):
        pass

    def jugar(self):
        pass


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
