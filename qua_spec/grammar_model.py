from typing import List, Dict, Union, Optional

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

    @property
    def is_primitive(self):
        return isinstance(self.type, PrimitiveData)

    @property
    def as_primitive_type_string(self):
        if not self.is_primitive:
            return None
        return {
            PrimitiveData.string: "string",
            PrimitiveData.number: "number",
            PrimitiveData.boolean: "boolean",
        }.get(self.type)

    def find_datatype(self, grammar: 'GrammarModel') -> Optional['DataType']:
        t = self.find_type(grammar)
        return t if isinstance(t, DataType) else None

    def find_type(self, grammar: 'GrammarModel') -> Optional[Union['EnumType', 'DataType', 'UnionType']]:
        if not self.is_primitive:
            return grammar.types[self.type]
        return None


@dataclass
class TypeProperty:
    name: str
    type: TypeReference


@dataclass
class PredefinedValidationInfo:
    original: str
    property: str
    name: str
    args: List[str]


@dataclass
class TypeValidation:
    type_name: str
    name: str
    description: str
    rule: str
    predefined: Optional[PredefinedValidationInfo]

    def validation_ast(self):
        import jmespath
        if self.rule is None:
            return None
        return jmespath.compile(self.rule)


@dataclass
class DataType(BaseType):
    name: str
    properties: Dict[str, TypeProperty]
    validations: List[TypeValidation]

    @property
    def is_data(self):
        return True

    def in_unions(self, grammar: 'GrammarModel') -> List['UnionType']:
        return [t for t in grammar.types.values() if isinstance(t, UnionType) and self.name in t.types]

    def friend_datatypes(self, grammar: 'GrammarModel') -> List[str]:
        collected = []
        for union in self.in_unions(grammar):
            collected.extend([n.name for n in union.find_datatypes(grammar)])
        return list(set(collected) - set([self.name]))


@dataclass
class UnionType(BaseType):
    name: str
    types: List[str]

    @property
    def is_union(self):
        return True

    def find_datatypes(self, grammar: 'GrammarModel') -> List['DataType']:
        collected = []
        for typename in self.types:
            t = grammar.types[typename]
            if isinstance(t, DataType):
                collected.append(t)
        return collected

    def find_datatypes_recursively(self, grammar: 'GrammarModel') -> List['DataType']:
        collected = []
        for typename in self.types:
            t = grammar.types[typename]
            if isinstance(t, UnionType):
                collected.extend(t.find_datatypes_recursively(grammar))
            elif isinstance(t, DataType):
                collected.append(t)
        return collected

    def find_unions(self, grammar: 'GrammarModel') -> List['UnionType']:
        collected = []
        for typename in self.types:
            t = grammar.types[typename]
            if isinstance(t, UnionType):
                collected.append(t)
                collected.extend(t.find_unions(grammar))
        return collected


@dataclass
class GrammarModel:
    version: str
    types: Dict[str, Union[
        EnumType,
        DataType,
        UnionType
    ]]
