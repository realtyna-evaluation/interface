from dataclasses import asdict, dataclass

JSONSerializableUUID = str


@dataclass
class BaseData:
    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
