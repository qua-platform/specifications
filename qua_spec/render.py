from typing import List, Any, Optional
from jinja2 import Environment, select_autoescape, FileSystemLoader
from dataclasses import dataclass
import os


@dataclass
class RenderingEnv:
    block_start_string: Optional[str] = None
    block_end_string: Optional[str] = None
    variable_start_string: Optional[str] = None
    variable_end_string: Optional[str] = None
    comment_start_string: Optional[str] = None
    comment_end_string: Optional[str] = None


@dataclass
class RenderJob:
    template: str
    output: str
    data: Any


@dataclass
class RenderConfig:
    output: str
    templates: str
    jobs: List[RenderJob]
    env: Optional[RenderingEnv] = None


def render(config: RenderConfig):
    env = Environment(
        loader=FileSystemLoader(config.templates),
        autoescape=select_autoescape()
    )
    if not os.path.exists(config.output):
        os.mkdir(config.output)
    for job in config.jobs:
        tpl = env.get_template(job.template)
        output = tpl.render(**job.data)
        output_file = os.path.join(config.output, job.output)
        with open(output_file, "w+") as f:
            f.write(output)
