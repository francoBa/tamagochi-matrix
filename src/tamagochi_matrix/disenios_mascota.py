from abc import ABC, abstractmethod

# importado para testing
from .consola import ansi


class MascotaDisenio(ABC):
    """Clase base abstracta para cualquier diseño de mascota."""

    @abstractmethod
    def get_arte(self, estado: str) -> str:
        pass


class DisenioOriginal(MascotaDisenio):
    """
    Contiene el arte ASCII original del ejercicio.
    Usar atributos es una forma válida y simple de almacenar el arte.
    """

    def __init__(self):
        self.inicio = "\n╔════════════════════════════════════╗\n║                                    ║\n║              ▄▀▄  ▄▀▄              ║\n║            ▄▀ ▄▀▄▀ ▄▀              ║\n║           ▄▀ ▀▄▀ ▄▀                ║\n║          ▄▀'^''^' ▀▄               ║\n║        ▄▀   ▄▀▄     ▀▄             ║\n║        ▀▄▄▄▀   ▀▄     ▀▄           ║\n║                 ▀      ▀           ║\n║                                    ║\n╚════════════════════════════════════╝\n"
        self.feliz = "\n╔════════════════════════════════════╗\n║                                    ║\n║                ▄   ▄               ║\n║              ▄▀▄▀▄▀▄▀              ║\n║            ▄▀ ▀▄▀ █                ║\n║           ▄▀ ^  ^  ▀▄              ║\n║         ▄▀   ▄█     ▀▄             ║\n║         ▀▄▄▄▀  ▀▄     ▀▄           ║\n║                 ▀      ▀           ║\n║                                    ║\n╚════════════════════════════════════╝\n"
        self.disgustado = "\n╔════════════════════════════════════╗\n║                                    ║\n║                                    ║\n║              ▄▀▀▀▄▀▀▄              ║\n║            ▄▀  ▄▀ ▄ ▄█             ║\n║           ▄▀ >  <  ▀▄              ║\n║         ▄▀   ▄█     ▀▄             ║\n║         ▀▄▄▄▀  ▀▄     ▀▄           ║\n║                 ▀      ▀           ║\n║                                    ║\n╚════════════════════════════════════╝\n"
        self.triste = "\n╔════════════════════════════════════╗\n║                                    ║\n║                                    ║\n║              ▄▀▀▀▄▀▀▄              ║\n║            ▄▀  ▄▀ ▄ ▄█             ║\n║           ▄▀ ╦  ╦  ▀▄              ║\n║         ▄▀   ▄█     ▀▄             ║\n║         ▀▄▄▄▀  ▀▄     ▀▄           ║\n║                 ▀      ▀           ║\n║                                    ║\n╚════════════════════════════════════╝\n"
        self.muerto = "\n╔════════════════════════════════════╗\n║                                    ║\n║                                    ║\n║               ▄▄  ▄▄               ║\n║             ▄▀ ▄▀▀▄ █▄             ║\n║           ▄▀ X  X  ▀▄              ║\n║         ▄▀   ▄█     ▀▄             ║\n║         ▀▄▄▄▀  ▀▄     ▀▄           ║\n║                 ▀      ▀           ║\n║                                    ║\n╚════════════════════════════════════╝\n"

    def get_arte(self, estado: str) -> str:
        """
        Devuelve el arte correspondiente al estado.
        Usamos getattr para acceder al atributo por su nombre en string.
        """
        return getattr(self, estado, self.inicio)


# --- Bloque de Prueba y Demostración ---
if __name__ == "__main__":
    print(f"{ansi.BOLD}--- DEMOSTRACIÓN DEL MÓDULO DE DISEÑOS ---{ansi.RESET}")

    mi_diseño = DisenioOriginal()

    estados_a_probar = [
        "inicio",
        "feliz",
        "triste",
        "disgustado",
        "muerto",
        "estado_invalido",
    ]

    for estado in estados_a_probar:
        print(f"\n{ansi.YELLOW}--- Probando estado: '{estado}' ---{ansi.RESET}")

        arte = mi_diseño.get_arte(estado)

        print(f"{ansi.GREEN}{arte}{ansi.RESET}")

    print(f"\n{ansi.BOLD}--- FIN DE LA DEMOSTRACIÓN ---{ansi.RESET}")
