import itertools
from dataclasses import dataclass
import re
from typing import List

from qua_spec.grammar_model import TypeValidation, DataType, PredefinedValidationInfo


@dataclass
class ParsedPredefinedValidation:
    predefined: str
    rule: str
    name: str
    description: str
    field: str


def expand_predefined(txt: str, t: DataType) -> List[TypeValidation]:
    return list(itertools.chain.from_iterable([
        it(txt, t)
        for it in [
            _not_empty,
            _is_integer,
            _in_range
        ]
    ]))


def _not_empty(txt: str, t: DataType) -> List[TypeValidation]:
    # name is not empty
    m = re.match(r"^(\w+)\s+is\s+not\s+empty$", txt.strip())
    if m:
        prop = m.group(1)
        return [
            TypeValidation(
                type_name=t.name,
                name=f"{prop}_not_empty",
                description=f"field `{prop}` of `{t.name}` must not be empty",
                rule=f"length(node.{prop}) >= `1`",
                predefined=PredefinedValidationInfo(
                    original=txt,
                    property=prop,
                    name="string_not_empty",
                    args=[]
                )
            )
        ]

    return []


def _is_integer(txt: str, t: DataType) -> List[TypeValidation]:
    # size is an integer
    m = re.match(r"^(\w+)\s+is\s+integer$", txt.strip())
    if m:
        prop = m.group(1)
        return [
            TypeValidation(
                type_name=t.name,
                name=f"{prop}_is_integer",
                description=f"field `{prop}` of `{t.name}` must be an integer",
                rule=f"ceil(node.{prop}) == node.{prop}",
                predefined=PredefinedValidationInfo(
                    original=txt,
                    property=prop,
                    name="is_integer",
                    args=[]
                )
            )
        ]

    return []


def _in_range(txt: str, t: DataType) -> List[TypeValidation]:
    # size is an integer
    m = re.match(r"^(\w+)\s+is\s+between\s+([^\s]+)\s+and\s+([^\s]+)", txt.strip())
    if m:
        prop = m.group(1)
        fromvalue = float(m.group(2))
        tovalue = float(m.group(3))
        return [
            TypeValidation(
                type_name=t.name,
                name=f"{prop}_is_between",
                description=f"field `{prop}` of `{t.name}` must be between {fromvalue} and {tovalue} " +
                            f"[received={'{{'}{prop}{'}}'}]",
                rule=f"node.{prop} >= `{fromvalue}` && node.{prop} <= `{tovalue}`",
                predefined=PredefinedValidationInfo(
                    original=txt,
                    property=prop,
                    name="number_in_range",
                    args=[str(fromvalue), str(tovalue)]
                )
            )
        ]

    return []