from abc import ABC, abstractmethod


class GameCharacter(ABC):
    """Base class for all characters: heroes, monsters and NPS"""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        # self.biography = str()

        # self.health_points = int()
        # self.protection = int()

    @abstractmethod
    def get_short_info(self) -> dict:
        pass
