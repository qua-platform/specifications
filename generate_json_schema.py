from qua_spec import load_grammar, render, RenderJob, RenderConfig, RenderingEnv


def generate():
    grammar = load_grammar(1)

    render(RenderConfig(
        output="build",
        templates="templates",
        env=RenderingEnv(
            filters={
            }
        ),
        output_transform=prettify_json,
        jobs=[
            RenderJob(
                template="json_schema.jinja2",
                output=f"qua1.schema.json",
                data={"grammar": grammar}
            )
        ]
    ))


def prettify_json(s: str) -> str:
    import json
    j = json.loads(s)
    return json.dumps(j, indent=2)


if __name__ == '__main__':
    generate()
