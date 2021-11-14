import qua_spec.grammar_model as model


def props(*args: model.TypeProperty):
    return {
        p.name: p for p in args
    }


def types(*args: model.BaseType):
    return {
        p.name: p for p in args
    }
