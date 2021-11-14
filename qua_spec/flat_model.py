from dataclasses import dataclass
from typing import List


@dataclass
class BaseType:
    name: str
    pass


@dataclass
class UnionType(BaseType):
    options: List[str]


@dataclass
class EnumType(BaseType):
    values: List[str]


@dataclass
class PropertyDefinition:
    name: str
    type_ref: str
    collection: bool = False


@dataclass
class DataType(BaseType):
    properties: List[PropertyDefinition]


class Grammar:
    def __init__(self) -> None:
        super().__init__()
        self._types = []

    def data(self, name: str, properties: List[PropertyDefinition]):
        self._types.append(DataType(
            name=name,
            properties=properties
        ))

    def union(self, name: str, options: List[str]):
        self._types.append(UnionType(
            name=name,
            options=options
        ))

    def enum(self, name: str, values: List[str]):
        self._types.append(EnumType(
            name=name,
            values=values
        ))
