try:
    from PIL import Image
except ImportError:
    Image = None


def convertir_imagen_a_ansi_bloques(ruta_archivo: str, ancho: int = 40) -> str:
    """
    Convierte un archivo de imagen a ANSI art usando la técnica de "bloques".
    Cada carácter de la terminal se usa como un píxel, estableciendo su
    color de fondo.

    Esta es una versión modernizada y adaptada de la librería 'ansiart'.

    Args:
        ruta_archivo: La ruta al archivo de imagen (PNG, JPG, etc.).
        ancho: El ancho deseado del arte final en caracteres.

    Returns:
        Un string que contiene el ANSI art listo para ser impreso.
    """
    if Image is None:
        return "Error: La librería 'Pillow' es necesaria. Instálala con 'pip install Pillow'"

    try:
        img_original = Image.open(ruta_archivo)
    except FileNotFoundError:
        print(f"ADVERTENCIA: No se encontró el archivo de imagen: {ruta_archivo}")
        return ""
    # Añadimos un except más genérico por si el archivo está corrupto (ej. 0 KB)
    except Exception as e:
        print(
            f"ADVERTENCIA: No se pudo abrir la imagen '{ruta_archivo}'. Puede estar corrupta. Error: {e}"
        )
        return ""

    img_rgb = img_original.convert("RGB")

    # 1. Definimos el alto de los caracteres. Siempre será la mitad del ancho.
    alto_caracteres = int(ancho * 0.5)

    # 2. Redimensionamos la imagen a las dimensiones finales de píxeles.
    #    Como la imagen de entrada es cuadrada, esto no la distorsionará.
    img_final = img_rgb.resize(
        (ancho, ancho)
    )  # Redimensiona a un cuadrado de 'ancho' x 'ancho'

    arte_final = []
    for y in range(alto_caracteres):
        for x in range(ancho):
            # Mapeamos la fila de caracteres a la fila de píxeles (saltando una de cada dos)
            y_pixel = y * 2
            coordenadas = (x, y_pixel)
            pixel = img_final.getpixel(coordenadas)

            if isinstance(pixel, (list, tuple)) and len(pixel) == 3:
                r, g, b = pixel
                arte_final.append(f"\033[48;2;{r};{g};{b}m \033[0m")
            else:
                arte_final.append("\033[48;2;0;0;0m \033[0m")

        arte_final.append("\n")

    return "".join(arte_final).rstrip()
