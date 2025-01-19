import abc

from .observer import Observer

class Subject(abc.ABC):

    def __init__(self) -> None:
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        self._observers.remove(obs)

    def notify_observers(self, method_name: str, obj: 'GameObject') -> None:
        for observer in self._observers:
            if hasattr(observer, method_name):
                getattr(observer, method_name)(obj)
            else:
                raise AttributeError(f"Observer does not have method {method_name}")