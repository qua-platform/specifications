import yaml

import qua_spec.model as model

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


def load_grammar() -> model.Model:
    return _load_yaml(yaml.safe_load(pkg_resources.read_text("qua_spec", "grammar.yaml")))
    pass


def _load_yaml_file(file):
    with open(file, "r") as f:
        data = yaml.load(f)

    return _load_yaml(data)


def _load_yaml(data):
    return model.Model(
        types={
            name: _type_from_dict(name, data) for name, data in data["types"].items()
        }
    )


def _type_from_dict(name: str, data: dict):
    if "data" in data:
        return model.DataType(name=name, properties={
            name: _to_property(name, value) for name, value in data["data"].items()
        })
    if "union" in data:
        return model.UnionType(name=name, types=data["union"])
    if "enum" in data:
        return model.EnumType(name=name, values=data["enum"])
    pass


def _to_property(name: str, value):
    if type(value) is str:
        return model.TypeReference(
            type=_str_to_property(name, value),
            list=False
        )
    else:
        # we assume this is a list
        return model.TypeReference(
            type=_str_to_property(name, value[0]),
            list=True
        )


def _str_to_property(name: str, value: str):
    is_primitive = value[0] == value[0].lower()
    if is_primitive:
        if value == "number":
            return model.PrimitiveData.number
        if value == "boolean":
            return model.PrimitiveData.boolean
        if value == "string":
            return model.PrimitiveData.string
        raise Exception(f"unknown primitive {value} in property {name}")
    else:
        return value
