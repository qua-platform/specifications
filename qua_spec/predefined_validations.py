from qua_spec.grammar_model import TypeValidation, DATA_TYPE_PLACEHOLDER


def is_integer(field_name: str) -> TypeValidation:
    return TypeValidation(
        "",
        name=f"{field_name}_is_integer",
        description=f"field `{field_name}` of `{DATA_TYPE_PLACEHOLDER}` must be an integer",
        code=f"math.ceil(node.{field_name}) == node.{field_name}"
    )
