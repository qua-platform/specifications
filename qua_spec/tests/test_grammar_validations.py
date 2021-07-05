import pytest
from qua_spec.grammar import load_grammar
import os

@pytest.mark.parametrize("grammar", [1,2])
def test_json_validation_for_grammars(grammar):
    from jsonschema import validate
    import yaml
    import json
    with open(os.path.abspath(__file__ + "/../../ast_definition.schema.json"), "r+") as f:
        schema = json.loads(f.read())
    with open(os.path.abspath(f"{__file__ }/../../qua{grammar}_grammar.yaml"), "r+") as f:
        grammar = yaml.safe_load(f.read())
    validate(instance=grammar, schema=schema)