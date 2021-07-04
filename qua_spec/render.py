from typing import List, Any, Optional, Dict, Callable
from jinja2 import Environment, select_autoescape, FileSystemLoader
from dataclasses import dataclass
import shutil
import os


@dataclass
class RenderingEnv:
    block_start_string: Optional[str] = None
    block_end_string: Optional[str] = None
    variable_start_string: Optional[str] = None
    variable_end_string: Optional[str] = None
    comment_start_string: Optional[str] = None
    comment_end_string: Optional[str] = None
    filters: Optional[Dict[str, Callable]] = None

    def to_jinja_env_args(self):
        d = {
            "block_start_string": self.block_start_string,
            "block_end_string": self.block_end_string,
            "variable_start_string": self.variable_start_string,
            "variable_end_string": self.variable_end_string,
            "comment_start_string": self.comment_start_string,
            "comment_end_string": self.comment_end_string,
        }
        return {
            name: value
            for name, value in d.items() if value is not None
        }


@dataclass
class RenderJob:
    template: str
    output: str
    data: Any


def _default_clear_callback(output: str):
    shutil.rmtree(output, ignore_errors=True)


@dataclass
class RenderConfig:
    output: str
    templates: str
    jobs: List[RenderJob]
    env: Optional[RenderingEnv] = None
    clear_callback: Callable[[str], None] = _default_clear_callback
    output_transform: Callable[[str], str] = lambda x: x


_default_env = Environment()


def render(config: RenderConfig):
    extra_env = config.env.to_jinja_env_args() if config.env is not None else {}
    env = Environment(
        loader=FileSystemLoader(config.templates),
        autoescape=select_autoescape(),
        **extra_env
    )
    # add filters
    if config.env is not None and config.env.filters is not None:
        for name, filter in config.env.filters.items():
            env.filters[name] = filter

    config.clear_callback(config.output)
    os.makedirs(config.output, exist_ok=True)
    for job in config.jobs:
        tpl = env.get_template(job.template)
        output = tpl.render(**job.data)
        output_file = os.path.join(config.output, job.output)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w+") as f:
            if config.output_transform:
                output = config.output_transform(output)
            f.write(output)
