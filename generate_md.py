from qua_spec import load_grammar, render, RenderJob, RenderConfig, RenderingEnv


def generate():
    grammar = load_grammar(2)

    render(RenderConfig(
        output="build",
        templates="templates",
        env=RenderingEnv(
            filters={
            }
        ),
        jobs=[
            RenderJob(
                template="md.jinja2",
                output=f"qua2_grammar.md",
                data={"grammar": grammar}
            )
        ]
    ))


if __name__ == '__main__':
    generate()
