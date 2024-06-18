

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
import weakref

if TYPE_CHECKING:
    from realtyna_interface.models.observe import ObservableModelMixin, FixedObservableModelMixin


class ObserverInterface(ABC):

    @property
    @abstractmethod
    def after_save(self) -> bool:
        pass

    @abstractmethod
    def get_subject(self) -> "ObservableModelMixin":
        pass

    @abstractmethod
    def update(self) -> None:
        pass



class AbstractObserver(ObserverInterface, ABC):
    def __init__(self, model: "FixedObservableModelMixin") -> None:
        super().__init__()
        self.model_ref = weakref.ref(model)

    def get_subject(self) -> "FixedObservableModelMixin":
        return self.model_ref()
