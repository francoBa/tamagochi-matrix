from abc import ABC, abstractmethod


class MascotaDiseño(ABC):
    """Clase base abstracta para cualquier diseño de mascota."""

    @abstractmethod
    def get_arte(self, estado: str) -> str:
        pass
