from qua_spec.grammar_model import DataType
from qua_spec.qua1_grammar import grammar as qua1
from qua_spec.qua2_grammar import grammar as qua2
import qua_spec.tests.validation_asts as validation_asts

grammars = [qua1, qua2]

qua1_validations = [
    (t, v, name, ast)
    for t in qua1.types.values() if isinstance(t, DataType)
    for v in t.validations
    for name, ast in getattr(validation_asts, f"{t.name}_{v.name}", {}).items()
]

# aaa = [
#     (t, v, f"{t.name}_{v.name}")
#     for t in qua1.types.values() if isinstance(t, DataType)
#     for v in t.validations
# ]