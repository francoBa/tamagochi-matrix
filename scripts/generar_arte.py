import sys
import os
import argparse
import re
from string import Template

# Añadimos la ruta a src para poder importar nuestro convertidor
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from tamagochi_matrix.convertidor_arte import convertir_imagen_a_ansi_bloques


def validar_nombre_clase(nombre: str) -> bool:
    """Valida si un string es un identificador válido para una clase de Python."""
    return re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", nombre) is not None


def generar_codigo_diseño(nombre_clase: str, mapa_estado_archivo: dict):
    """
    Genera un archivo .py completo para una nueva clase de Diseño
    directamente en la carpeta de diseños del proyecto.
    """
    # --- Construcción del código ---
    codigo_final = f"import time\n"  # Necesario para el bloque de prueba
    codigo_final += f"from string import Template\n"
    codigo_final += f"from .base import MascotaDiseño\n\n"
    codigo_final += f"class {nombre_clase}(MascotaDiseño):\n"
    codigo_final += "    def __init__(self):\n"
    codigo_final += "        self.plantillas = {\n"

    for estado, nombre_archivo in mapa_estado_archivo.items():
        # La ruta se construye relativa a la ubicación del script
        ruta_completa = os.path.join(
            os.path.dirname(__file__), "../imagenes_fuente", nombre_archivo
        )
        print(f"Procesando '{estado}': {ruta_completa}...")

        # Validación de existencia de archivos (redundante pero seguro)
        if not os.path.exists(ruta_completa):
            print(
                f"\n{_color_rojo('Error:')} No se pudo encontrar el archivo: {ruta_completa}"
            )
            return

        arte_generado = convertir_imagen_a_ansi_bloques(ruta_completa)
        arte_generado_escapado = arte_generado.replace('"""', '\\"\\"\\"')

        codigo_final += (
            f'            "{estado}": Template("""\n{arte_generado_escapado}"""),\n'
        )

    codigo_final += "        }\n"
    # Asignación explícita a prueba de linters para el valor por defecto.
    codigo_final += '        if "inicio" in self.plantillas:\n'
    codigo_final += (
        '            self.plantillas["default"] = self.plantillas["inicio"]\n'
    )
    codigo_final += '        elif "feliz" in self.plantillas:\n'
    codigo_final += (
        '            self.plantillas["default"] = self.plantillas["feliz"]\n\n'
    )

    codigo_final += "    def get_arte(self, estado):\n"
    codigo_final += (
        '        plantilla = self.plantillas.get(estado, self.plantillas["default"])\n'
    )
    codigo_final += "        return plantilla.substitute()\n\n"

    ### AÑADIMOS EL BLOQUE DE PRUEBA AUTOMÁTICO ###
    codigo_final += f"# --- Bloque de Prueba y Demostración ---\n"
    codigo_final += f'if __name__ == "__main__":\n'
    codigo_final += f"    diseño = {nombre_clase}()\n"
    codigo_final += (
        f'    print("--- DEMO: Mostrando todos los estados de {nombre_clase} ---")\n'
    )
    codigo_final += (
        f'    estados = ["inicio", "feliz", "triste", "disgustado", "muerto"]\n'
    )
    codigo_final += f"    for estado in estados:\n"
    codigo_final += f'        print(f"\\n--- Estado: {{estado}} ---")\n'
    codigo_final += f"        print(diseño.get_arte(estado))\n"
    codigo_final += f"        time.sleep(1.5)\n"
    codigo_final += f'    print("\\n--- FIN DE LA DEMO ---")\n'

    # --- Guardado del archivo ---
    nombre_archivo_salida = f"{nombre_clase.lower()}.py"
    ruta_salida = os.path.join(
        os.path.dirname(__file__),
        f"../src/tamagochi_matrix/disenios/{nombre_archivo_salida}",
    )
    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(codigo_final)

    print(f"\n{_color_verde('¡Listo!')} Se ha creado el nuevo diseño en:")
    print(f"  -> {ruta_salida}")
    print("El juego ahora podrá usar este diseño automáticamente.")


def _color_rojo(texto):
    return f"\033[91m{texto}\033[0m"


def _color_verde(texto):
    return f"\033[92m{texto}\033[0m"


class ArgumentParserError(Exception):
    pass


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise ArgumentParserError(message)


def main():
    parser = CustomArgumentParser(
        description="Generador de clases de Diseño para Tamagochi Matrix.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )

    # --- Argumentos Nombrados ---
    parser.add_argument(
        "nombre_clase",
        metavar="NOMBRE_CLASE",
        help="El nombre para la clase de Python (ej. DisenioMerovingio).",
    )
    parser.add_argument(
        "--inicio", required=True, help="Archivo de imagen para el estado 'inicio'."
    )
    parser.add_argument(
        "--feliz", required=True, help="Archivo de imagen para el estado 'feliz'."
    )
    parser.add_argument(
        "--triste", required=True, help="Archivo de imagen para el estado 'triste'."
    )
    parser.add_argument(
        "--disgustado",
        required=True,
        help="Archivo de imagen para el estado 'disgustado' (usado cuando está crítico o hambriento).",
    )
    parser.add_argument(
        "--muerto", required=True, help="Archivo de imagen para el estado 'muerto'."
    )
    parser.add_argument(
        "-h",
        "--ayuda",
        action="help",
        default=argparse.SUPPRESS,
        help="Muestra este mensaje de ayuda y sale.",
    )

    try:
        args = parser.parse_args()
    except ArgumentParserError:
        print(
            f"\n{_color_rojo('Error de argumentos:')} Faltan argumentos o son incorrectos."
        )
        print(f"Por favor, utiliza '-h' o '--ayuda' para ver las instrucciones de uso.")
        sys.exit(1)

    # --- Validaciones Personalizadas ---
    if not validar_nombre_clase(args.nombre_clase):
        print(
            f"\n{_color_rojo('Error:')} El nombre de la clase '{args.nombre_clase}' no es válido."
        )
        print(
            "Debe empezar con una letra o guion bajo, y solo contener letras, números y guiones bajos."
        )
        return

    # Creamos el diccionario a partir de los argumentos nombrados
    mapa_archivos = {
        "inicio": args.inicio,
        "feliz": args.feliz,
        "triste": args.triste,
        "disgustado": args.disgustado,
        "muerto": args.muerto,
    }

    generar_codigo_diseño(args.nombre_clase, mapa_archivos)


if __name__ == "__main__":
    main()
