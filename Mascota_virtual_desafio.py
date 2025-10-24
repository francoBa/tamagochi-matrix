# importar el modulo random
# import imagen desde el archivo mascota.py
from random import randint
from mascota import imagen

class MascotaVirtual:
    def __init__(self, nombre):
        self.nombre = nombre
        self.felicidad = 0
        self.hambre = 100
        self.imagen = imagen.inicio
        self.imagen_feliz = imagen.feliz
        self.imagen_disgustado = imagen.disgustado
        self.imagen_triste = imagen.triste
        self.imagen_muerto = imagen.muerto

    def alimentar(self):
        self.felicidad -= randint(5, 10)
        if self.felicidad < 0: self.felicidad = 0
        if self.hambre == 0:
            print(self.imagen_disgustado)
            print(f"{self.nombre}, está lleno. Ya no puede comer más!")
        else:
            self.hambre -= randint(10, 15)
            if self.hambre < 0: self.hambre = 0
            print(self.imagen_feliz)
            print(f"{self.nombre} has sido alimentado")

    def jugar(self):
        pass

    def estado_animo(self):
        pass

    def presentacion(self):
        print(
            f"\n╔════════════════════════════════════╗\n║     Te presento a tu mascota!      ║\n╚════════════════════════════════════╝\n{self.imagen}\tSu nombre es {self.nombre}"
        )

    def despedida(self):
        print(
            f"\n╔════════════════════════════════════╗\n║             Nos vemos!             ║\n╚════════════════════════════════════╝{self.imagen}╔════════════════════════════════════╗\n║        Jueguemos otro día!         ║\n╚════════════════════════════════════╝\n"
        )

interfaz_inicio = "\n╔════════════════════════════════════╗\n║       Bienvenido a tu primer       ║\n║          mascota virtual!          ║\n╚════════════════════════════════════╝\n"
interfaz_juego = "\n╔════════════════════════════════════╗\n║       Opciones disponibles:        ║\n║                                    ║\n║ 1 - Alimentar                      ║\n║ 4 - Salir                          ║\n║                                    ║\n╚════════════════════════════════════╝\n"


print(interfaz_inicio)
nombre = input("Elige un nombre para tu mascota: ").strip()

mascota = MascotaVirtual(nombre)
mascota.presentacion()

while True:
    print(interfaz_juego)
    opcion = input("Elige una opción: ").strip()

    match opcion:
        case "1":
            mascota.alimentar()
        case "4":
            mascota.despedida()
            break

# Crear una instancia de MascotaVirtual

# Interactuar con la mascota virtual
# alimenta, juega y muestra su estado de animo
# repite esta accion al menos 8 veces

# Si te animas crea una interfaz para poder interactuar con tu mascota
