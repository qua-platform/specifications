from qua_spec import load_grammar, render, RenderJob, RenderConfig, RenderingEnv
from qua_spec.grammar_model import GrammarModel


def generate():
    grammar = load_grammar(2)
    used_nodes = set("Program")
    root = grammar.types["Program"]
    nodes = [root]
    for node in nodes:
        for t in node.dependent_types(grammar):
            if t.name in used_nodes:
                pass
            else:
                nodes.append(t)
                used_nodes.add(t.name)

    for t in grammar.types.values():
        if t.name not in used_nodes:
            nodes.append(t)
            used_nodes.add(t.name)
    grammar = GrammarModel(
        version=grammar.version,
        types={t.name: t for t in nodes}
    )

    render(RenderConfig(
        output="build",
        templates="templates",
        env=RenderingEnv(
            filters={
            }
        ),
        jobs=[
            RenderJob(
                template="py2.jinja2",
                output=f"qua2_grammar.py",
                data={"grammar": grammar}
            )
        ]
    ))


if __name__ == '__main__':
    generate()
