from qua_spec.render import render, RenderConfig, RenderJob
import os


def test_render():
    render(config=RenderConfig(
        output="out",
        templates=f"{os.path.join(__file__, '../templates')}",
        jobs=[
            RenderJob(
                "oop.jinja2",
                "out1.kt",
                {
                    "name": "Class1"
                }
            ),
            RenderJob(
                "oop.jinja2",
                "out2.kt",
                {
                    "name": "Class2"
                }
            )
        ]
    ))
