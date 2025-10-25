# Importamos la clase que queremos probar desde nuestro paquete instalado
from tamagochi_matrix.logica_mascota import MascotaLogica


def test_creacion_mascota():
    """Prueba que la mascota se crea con los valores iniciales correctos."""
    mascota = MascotaLogica("Testy")
    assert mascota.nombre == "Testy"
    assert mascota.hambre == 50
    assert mascota.felicidad == 51
    assert mascota.esta_viva is True


def test_estado_feliz_inicial():
    """Prueba que el estado inicial de la mascota es 'feliz'."""
    mascota = MascotaLogica("Testy")
    info = mascota.get_info_estado()
    assert info["clave"] == "feliz"


def test_alimentar_reduce_hambre():
    """Prueba que la función alimentar reduce el hambre."""
    mascota = MascotaLogica("Testy")
    hambre_inicial = mascota.hambre
    mascota.alimentar()
    assert mascota.hambre < hambre_inicial
