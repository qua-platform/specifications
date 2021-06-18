from typing import List, Dict, Union

from dataclasses import dataclass
from enum import Enum


class PrimitiveData(Enum):
    number = 0
    boolean = 1
    string = 2


class BaseType:
    @property
    def is_data(self):
        return False

    @property
    def is_union(self):
        return False

    @property
    def is_enum(self):
        return False


@dataclass
class EnumType(BaseType):
    name: str
    values: List[str]

    @property
    def is_enum(self):
        return True


@dataclass
class TypeReference:
    type: Union[str, PrimitiveData]
    list: bool


@dataclass
class TypeProperty:
    name: str
    type: TypeReference


@dataclass
class DataType(BaseType):
    name: str
    properties: Dict[str, TypeProperty]

    @property
    def is_data(self):
        return True


@dataclass
class UnionType(BaseType):
    name: str
    types: List[str]

    @property
    def is_union(self):
        return True


@dataclass
class Model:
    types: Dict[str, Union[
        EnumType,
        DataType,
        UnionType
    ]]
