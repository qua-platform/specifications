FROM gitpod/workspace-full

# Install custom tools, runtime, etc.
RUN pip install poetry
RUN poetry config virtualenvs.create false