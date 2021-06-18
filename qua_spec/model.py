from typing import List, Dict, Union

from dataclasses import dataclass
from enum import Enum


class PrimitiveData(Enum):
    number = 0
    boolean = 1
    string = 2


@dataclass
class EnumType:
    name: str
    values: List[str]


@dataclass
class TypeReference:
    type: Union[str, PrimitiveData]
    list: bool


@dataclass
class TypeProperty:
    name: str
    type: TypeReference


@dataclass
class DataType:
    name: str
    properties: Dict[str, TypeProperty]


@dataclass
class UnionType:
    name: str
    types: List[str]


@dataclass
class Model:
    types: Dict[str, Union[
        EnumType,
        DataType,
        UnionType
    ]]
