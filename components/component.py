from abc import ABC, abstractmethod

from pygame import Surface
from pygame.event import Event


class Component(ABC):
    def __init__(self, screen: Surface) -> None:
        super().__init__()
        self._screen = screen

    @abstractmethod
    def update_events(self, events: list[Event]) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass
