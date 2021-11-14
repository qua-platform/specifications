from dataclasses import dataclass
from typing import List, Union, Dict

from qua_spec.grammar_model import GrammarModel


@dataclass
class AstNode:
    """
    A node in a specific AST. This is an instance of some type from the grammar model
    """
    _type: str
    _grammar: GrammarModel
    _properties: Dict[str, Union['AstNode', List['AstNode']]]

    def __getattr__(self, item):
        if item in self._properties:
            return self._properties[item]
        return None

    @staticmethod
    def from_dict(d: dict, grammar: GrammarModel):
        return AstNode._from_dict(d, [], grammar)

    @staticmethod
    def _from_dict(d: dict, path: List[str], grammar: GrammarModel):
        the_type = d["type"]
        data = d["data"]
        if the_type not in grammar.types:
            raise MissingTypeException(type_name=the_type)
        type_model = grammar.types[the_type]
        props = {}
        for prop in type_model.properties.values():
            if prop.name not in data:
                raise MissingPropertyException(path, prop.name)
            if prop.type.is_primitive:
                props[prop.name] = data[prop.name]
            else:
                props[prop.name] = AstNode._from_dict(data[prop.name], [*path, prop.name], grammar)
        return AstNode(
            _type=the_type,
            _grammar=grammar,
            _properties=props
        )


class MissingPropertyException(Exception):
    def __init__(self, path: List[str], prop: str, *args: object) -> None:
        super().__init__(*args)
        self._path = [*path]
        self._prop = prop

    def __str__(self):
        return f"missing property '{self._prop}' in /{'/'.join(self._path)}"


class MissingTypeException(Exception):
    def __init__(self, type_name: str, *args: object) -> None:
        super().__init__(*args)
        self._type_name = type_name

    def __str__(self):
        return f"missing type '{self._type_name}' in grammar"
