import pytest

from qua_spec.ast_model import AstNode
from qua_spec.grammar_model import DataType, GrammarModel
from qua_spec.qua1_grammar import grammar as qua1
from qua_spec.qua2_grammar import grammar as qua2
import qua_spec.tests.validation_asts as validation_asts
import dataclasses

grammars = [qua1, qua2]


def remove_validations(grammar: GrammarModel) -> GrammarModel:
    return dataclasses.replace(
        grammar,
        types={
            t.name: t if not isinstance(t, DataType) else dataclasses.replace(t, validations=[])
            for t in grammar.types.values()
        }
    )


grammars_without_validations = [remove_validations(q) for q in grammars]


@pytest.mark.parametrize("grammar", grammars)
def test_qua_grammar_is_valid(grammar):
    available_types = [t.name for t in grammar.types.values()]
    for t in grammar.types:
        t


qua1_validations = [
    ((grammar_name, grammar_without_validation, grammar), t, v, name, ast)
    for grammar, grammar_without_validation, grammar_name in
    zip(grammars, grammars_without_validations, ["qua1", "qua2"])
    for t in grammar.types.values() if isinstance(t, DataType)
    for v in t.validations
    for name, ast in getattr(validation_asts, f"{t.name}_{v.name}", {}).items()

]


def validation_name(it):
    if type(it) is tuple and type(it[0]) is str:
        return it[0]
    if hasattr(it, "name"):
        return it.name
    elif isinstance(it, str):
        return it
    else:
        return ''


def add_validation(grammar, type_name, validations):
    return dataclasses.replace(
        grammar,
        types={
            t.name: t if t.name != type_name else dataclasses.replace(t, validations=validations)
            for t in grammar.types.values()
        }
    )


@pytest.mark.parametrize("grammar,datatype,validation,ast_name,ast", qua1_validations, ids=validation_name)
def test_validation_rules_of_qua1(grammar, datatype, validation, ast_name, ast):
    validation.code
    grammar_name, grammar_without_validation, full_grammar = grammar
    the_grammar = add_validation(grammar_without_validation, datatype.name, [validation])
    program = AstNode.from_dict(ast, the_grammar)
    def_name = f"{datatype.name}_{validation.name}"
    test_def = getattr(validation_asts, f"{datatype.name}_{validation.name}", None)
    assert test_def is not None, \
        f"expecting valid and invalid ASTs in `{def_name}` under package qua_spec.tests.validation_asts"
