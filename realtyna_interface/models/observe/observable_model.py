import typing
from typing import Any
import weakref
from django.db import models, transaction
from model_utils import FieldTracker
from realtyna_interface.models.observe import ObserverInterface, AbstractObserver



class ObservableModelMixin(models.Model):
    _tracker: typing.Optional[FieldTracker] = None
    __changed_fields: typing.Optional[dict] = None
    __being_created: typing.Optional[bool] = None
    __observers: typing.List[ObserverInterface] = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._initiate_observers()

    def _get_observers(self) -> typing.List[ObserverInterface]:
        raise NotImplementedError()

    def _initiate_observers(self) -> None:
        self.__observers = self._get_observers()

    @property
    def being_created(self) -> bool:
        return self.__being_created

    @property
    def changed_fields(self) -> typing.Optional[dict]:
        return self.__changed_fields

    def before_save_update(self):
        list(
            map(
                lambda observer: observer.update(),
                list(filter(lambda observer: not observer.after_save, self.__observers))
            )
        )

    def after_save_update(self):
        list(
            map(
                lambda observer: observer.update(),
                list(filter(lambda observer: observer.after_save, self.__observers))
            )
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        with transaction.atomic():
            self.__being_created = not bool(self.pk)
            if self._tracker is not None:
                self.__changed_fields = self._tracker.changed()
            self.before_save_update()
            super().save(force_insert, force_update, using, update_fields)
            self.after_save_update()

    class Meta:
        abstract = True


class FixedObservableModelMixin(ObservableModelMixin):
    observer_classes: typing.List[typing.Type[AbstractObserver]] = []

    def get_observer_classes(self) -> typing.List[typing.Type[AbstractObserver]]:
        return self.observer_classes

    def _get_observers(self) -> typing.List[ObserverInterface]:
        return list(
            map(
                lambda observer_class: observer_class(self), self.get_observer_classes()
            )
        )

    class Meta:
        abstract = True
