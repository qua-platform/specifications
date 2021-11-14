import pytest
from qua_spec.grammar_model import DataType
from qua_spec.qua1_grammar import grammar as qua1
from qua_spec.qua2_grammar import grammar as qua2
import qua_spec.tests.validation_asts as validation_asts

grammars = [qua1, qua2]


@pytest.mark.parametrize("grammar", grammars)
def test_qua_grammar_is_valid(grammar):
    available_types = [t.name for t in grammar.types.values()]
    for t in grammar.types:
        t


qua1_validations = [
    (t, v, name, ast)
    for t in qua1.types.values() if isinstance(t, DataType)
    for v in t.validations
    for name, ast in getattr(validation_asts, f"{t.name}_{v.name}", {}).items()
]


def validation_name(it):
    if hasattr(it, "name"):
        return it.name
    elif isinstance(it, str):
        return it
    else:
        return ''


@pytest.mark.parametrize("datatype,validation,ast_name,ast", qua1_validations, ids=validation_name)
def test_validation_rules_of_qua1(datatype, validation, ast_name, ast):
    validation.code
    def_name = f"{datatype.name}_{validation.name}"
    test_def = getattr(validation_asts, f"{datatype.name}_{validation.name}", None)
    assert test_def is not None, \
        f"expecting valid and invalid ASTs in `{def_name}` under package qua_spec.tests.validation_asts"
    assert "valid" in test_def and type(test_def["valid"]) is list, "valid should be a list"
    assert "invalid" in test_def and type(test_def["invalid"]) is list, "invalid should be a list"
