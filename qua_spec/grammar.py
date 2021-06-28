import yaml

import qua_spec.grammar_model as model

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


def load_grammar() -> model.GrammarModel:
    grammar_yaml = yaml.safe_load(pkg_resources.read_text("qua_spec", "grammar.yaml"))
    for imported in grammar_yaml.get("imports", []):
        loaded_import = yaml.safe_load(pkg_resources.read_text("qua_spec", f"{imported}.yaml"))
        del loaded_import["$schema"]
        for item in ["enums", "unions", "types"]:
            grammar_yaml = {
                **grammar_yaml,
                item: {
                    **(loaded_import.get(item, {}) if item in loaded_import else {}),
                    **grammar_yaml.get(item, {})
                }
            }
    grammar = _load_yaml(grammar_yaml)
    # make sure each type is defined
    for t in grammar.types.values():
        if isinstance(t, model.DataType):
            for prop in t.properties.values():
                if not prop.type.is_primitive and prop.type.type not in grammar.types.keys():
                    raise Exception(f"missing type {prop.type.type}. used in {t.name}.{prop.name}")
        if isinstance(t, model.UnionType):
            for typeinunion in t.types:
                if typeinunion not in grammar.types.keys():
                    raise Exception(f"missing type {typeinunion}. used in union {t.name}")
                elif grammar.types[typeinunion].is_enum:
                    raise Exception(f"union type {t.name} refers to enum type {typeinunion}")

    return grammar


def _load_yaml_file(file):
    with open(file, "r") as f:
        data = yaml.load(f)

    return _load_yaml(data)


def _load_yaml(data):
    return model.GrammarModel(
        version=data.get("version"),
        types={
            **{
                name: model.DataType(name=name, properties={
                    pname: _to_property(pname, pvalue) for pname, pvalue in data.items() if not pname.startswith("$")
                }, validations=[
                    model.TypeValidation(
                        type_name=name,
                        name=validation_name,
                        description=item if type(item) is str else item["description"],
                        rule=item["rule"] if "rule" in item else None
                    )
                    for validation_name, item in data.get("$validations", {}).items()
                ]) for name, data in data["types"].items()
            },
            **{
                name: model.EnumType(name=name, values=data) for name, data in data["enums"].items()
            },
            **{
                name: model.UnionType(name=name, types=data) for name, data in data["unions"].items()
            }
        }
    )


def _to_property(name: str, value):
    return model.TypeProperty(
        name=name,
        type=_to_type_reference(name, value)
    )


def _to_type_reference(name: str, value):
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
