import pytest
from qua_spec.grammar import load_grammar
from qua_spec.grammar_model import DataType

@pytest.mark.parametrize("grammar", [1,2])
def test_qua_grammar_is_loadable(grammar):
    load_grammar(grammar)


@pytest.mark.parametrize("grammar", [1,2])
def test_validate_all_rules_are_valid(grammar):
    import jmespath
    g = load_grammar(grammar)
    validations = [
        v
        for t in g.types if isinstance(t, DataType)
        for v in t.validations
    ]
    for v in validations:
        try:
            jmespath.compile(v.rule)
        except Exception as e:
            raise Exception(f"failed to compile validation rule {v.name} for node {v.type_name} in grammar {grammar}", e)


            