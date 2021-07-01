import yaml

from qua_spec.grammar import _load_yaml


def load_single_type(s):
    model = _load_yaml({
        "types": {
            "Type1": yaml.safe_load(s)
        }
    })
    assert len(model.types) == 1
    return list(model.types.values())[0]


def run_validation(validation, data):
    import jmespath
    return jmespath.search(validation.rule, {"node": data})


def test_not_empty_string():
    model = load_single_type("""
        strprop: string
        $validations:
            $predefined:
                - strprop is not empty
    """)

    assert len(model.validations) == 1
    predefined = model.validations[0].predefined
    assert predefined.name == "string_not_empty"
    assert predefined.property == "strprop"

    assert True is run_validation(model.validations[0], {"strprop": "some value"})
    assert False is run_validation(model.validations[0], {"strprop": ""})


def test_is_integer():
    model = load_single_type("""
        size: number
        $validations:
            $predefined:
                - size is integer
    """)

    assert len(model.validations) == 1
    predefined = model.validations[0].predefined
    assert predefined.name == "is_integer"
    assert predefined.property == "size"

    assert True is run_validation(model.validations[0], {"size": 5})
    assert True is run_validation(model.validations[0], {"size": 5.0})
    assert False is run_validation(model.validations[0], {"size": 3.4})


def test_in_range():
    model = load_single_type("""
        size: number
        $validations:
            $predefined:
                - size is between 8 and 100
    """)

    assert len(model.validations) == 1
    predefined = model.validations[0].predefined
    assert predefined.name == "number_in_range"
    assert predefined.property == "size"

    assert True is run_validation(model.validations[0], {"size": 20})
    assert True is run_validation(model.validations[0], {"size": 8})
    assert True is run_validation(model.validations[0], {"size": 100})
    assert False is run_validation(model.validations[0], {"size": 2})
