from qua_spec import load_grammar, render, RenderJob, RenderConfig, RenderingEnv


def generate():
    grammar = load_grammar()

    render(RenderConfig(
        output="build",
        templates="templates",
        env=RenderingEnv(
            filters={
            }
        ),
        jobs=[
            RenderJob(
                template="json_schema.jinja2",
                output=f"qua.schema.json",
                data={"grammar": grammar}
            )
        ]
    ))


if __name__ == '__main__':
    generate()
