from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List
from django_components.facade import ComponentFacade

from realtyna_interface.data import BaseData, JSONSerializableUUID


class ListingFacade(ComponentFacade, ABC):
    name: str = "listing"

    @abstractmethod
    def validate_listing(self, listing: JSONSerializableUUID) -> bool:
        pass


class ReservingFacade(ComponentFacade, ABC):
    name: str = "reserving"

    @dataclass
    class Reservation(BaseData):
        uid: JSONSerializableUUID
        reserver: str
        start_datetime: datetime
        end_datetime: datetime

    @abstractmethod
    def get_reservations_for_rooms(
        self,
        rooms: List[JSONSerializableUUID],
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> Reservation:
        pass
