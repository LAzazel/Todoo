from abc import ABC, abstractmethod
from typing import Callable


class IEventBus(ABC):
    @abstractmethod
    def publish(self, event) -> None: pass

    @abstractmethod
    def subscribe(self, event_type: type, handler: Callable) -> None: pass