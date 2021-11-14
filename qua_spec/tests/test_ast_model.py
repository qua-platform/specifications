import pytest

from qua_spec.ast_model import AstNode, MissingPropertyException, MissingTypeException
from qua_spec.grammar_model import GrammarModel, DataType, TypeProperty, TypeReference, PrimitiveData


def test_we_load_data_type():
    node = AstNode.from_dict({
        "type": "Program",
        "data": {}
    }, GrammarModel(
        "1",
        types={
            "Program": DataType(
                "Program",
                properties={},
                validations=[]
            )
        }

    ))

    assert node._type == "Program"


def test_we_fail_to_load_missing_property_on_data_type():
    with pytest.raises(MissingPropertyException, match="missing property 'name' in /"):
        AstNode.from_dict({
            "type": "Program",
            "data": {}
        }, GrammarModel(
            "1",
            types={
                "Program": DataType(
                    "Program",
                    properties={
                        "name": TypeProperty(
                            name="name",
                            type=TypeReference(PrimitiveData.string, list=False)
                        )
                    },
                    validations=[]
                )
            }

        ))


def test_we_load_primitive_property_data_type():
    node = AstNode.from_dict({
        "type": "Program",
        "data": {
            "name": "myprogram"
        }
    }, GrammarModel(
        "1",
        types={
            "Program": DataType(
                "Program",
                properties={
                    "name": TypeProperty(
                        name="name",
                        type=TypeReference(PrimitiveData.string, list=False)
                    )
                },
                validations=[]
            )
        }

    ))
    assert node._properties.keys() == {"name"}


def test_we_load_data_property_data_type():
    node = AstNode.from_dict({
        "type": "Program",
        "data": {
            "script": {
                "type": "Script",
                "data": {
                    "name": "myscript"
                }
            }
        }
    }, GrammarModel(
        "1",
        types={
            "Program": DataType(
                "Program",
                properties={
                    "script": TypeProperty(
                        name="script",
                        type=TypeReference("Script", list=False)
                    )
                },
                validations=[]
            ),
            "Script": DataType(
                "Script",
                properties={
                    "name": TypeProperty(
                        name="name",
                        type=TypeReference(PrimitiveData.string, list=False)
                    )
                },
                validations=[]
            )
        }
    ))
    assert node._properties.keys() == {"script"}
    assert node.script.name == "myscript"


def test_we_fail_non_existing_type():
    with pytest.raises(MissingTypeException):
        AstNode.from_dict({
            "type": "Program",
            "data": {}
        }, GrammarModel(
            "1",
            types={
            }

        ))
