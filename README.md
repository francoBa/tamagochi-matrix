# Tamagochi Matrix

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

[Instrucciones del desafío](/mascota_virtual.md)

Adopta una entidad digital y mantenla viva dentro de la Matrix. Un juego de mascota virtual para la terminal con una estética retro-digital.

---

## Demostración

![Demostración del Juego](https://github.com/user-attachments/assets/6cf38eba-9f96-4f28-aa78-1132c476be73)

---

## Acerca del Proyecto

`Tamagochi Matrix` es una reimaginación del clásico juego de mascota virtual, transportado a la estética icónica de la Matrix. En lugar de una mascota biológica, cuidas de una "entidad digital", gestionando su **Integridad** (salud) y **Conexión** (felicidad) para asegurar su supervivencia en la red.

El juego se ejecuta completamente en la terminal y utiliza arte ANSI a todo color generado a partir de imágenes para una experiencia visual única.

### Características

* **Estética Inmersiva:** Secuencia de inicio y fin con la icónica "lluvia digital" de Matrix.
* **Arte ANSI de Alta Calidad:** Las mascotas se renderizan con colores "True Color" para un detalle impresionante en terminales modernas.
* **Sistema de Carga Dinámica:** Añadir nuevas mascotas es tan fácil como generar un nuevo archivo de diseño. El juego las descubre y las añade a la selección aleatoria automáticamente.
* **Interfaz Clara:** Barras de progreso dinámicas, menús enmarcados y recomendaciones contextuales para una jugabilidad intuitiva.
* **Sonido y Retroalimentación:** Efectos de sonido para acciones clave que mejoran la experiencia.
* **Herramientas de Desarrollo Incluidas:** El proyecto viene con un potente script para convertir tus propias imágenes en nuevos diseños de mascotas.

---

## Instalación

Para instalar y ejecutar `Tamagochi Matrix`, necesitarás **Python 3.8+** y **Git**.

1. **Clona el repositorio:**

    ```bash
    git clone https://github.com/francoBa/tamagochi-matrix.git
    cd tamagochi-matrix
    ```

2. **Crea y activa un entorno virtual (recomendado):**

    ```bash
    # En Windows
    python -m venv env
    .\env\Scripts\activate

    # En macOS / Linux
    python3 -m venv env
    source env/bin/activate
    ```

3. **Instala el paquete:**
    Este comando leerá el archivo `pyproject.toml` e instalará el juego y todas sus dependencias (`Pillow`, `pyfiglet`, `playsound`).

    ```bash
    pip install .
    ```

---

## Uso

Una vez instalado, puedes ejecutar el juego desde cualquier lugar en tu terminal con el siguiente comando:

  ```bash
  matrix-pet
  ```

Sigue las instrucciones en pantalla para interactuar con tu mascota. Para salir del juego de forma segura en cualquier momento, presiona Ctrl+C.

---

## Flujo de Trabajo para Desarrolladores: Añadir Nuevas Mascotas

Este proyecto incluye una herramienta para crear tus propios diseños de mascotas.

Prepara tus imágenes: Consigue 5 imágenes (para los estados inicio, feliz, triste, disgustado, muerto) y colócalas en la carpeta imagenes_fuente/.

Ejecuta el script generador: Llama al script desde la raíz del proyecto, pasándole el nombre de la nueva clase y los nombres de los archivos de imagen con sus respectivos flags.

  ```Bash
  python scripts/generar_arte.py NombreDeTuDisenio --inicio img_inicio.png --feliz img_feliz.png --triste img_triste.png --disgustado img_disgustado.png --muerto img_muerto.png
  ```

¡Listo! El script creará automáticamente el archivo de diseño en src/tamagochi_matrix/disenios/. La próxima vez que ejecutes matrix-pet, tu nueva mascota podría ser elegida al azar.

---

## Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.
