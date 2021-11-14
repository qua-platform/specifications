import dataclasses
class ValidationsStore:
    def __init__(self, validations) -> None:
        super().__init__()

    def validate(self, name: str, node_data: dict):
        return []


def validate_qua(qua_dict, validations_map):
    pass


def apply_qua_validation(path, root_qua_dict, qua_node_dict, validations: ValidationsStore, stop_on_error=True):
    node_type = qua_node_dict["type"]
    node_data = qua_node_dict["data"]
    errors = validations.validate(node_type, node_data)
    if len(errors) > 0 and stop_on_error:
        return errors
    for child_prop, child_node in node_data:
        if not isinstance(child_node, list):
            for c in child_node:

    pass


