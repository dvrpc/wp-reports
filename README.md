## Commands

| Task                  | Command                                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Run in venv           | `ve/bin/sanic server:app [--dev]`                                                                                 |
| Change python version | Modify postCreateCommand in .devcontainer/devcontainer.json                                                       |
| Format                | `ve/bin/ruff format`                                                                                              |
| Lint                  | `ve/bin/ruff check`                                                                                               |
| Add packages          | `uv pip install --python ve/bin/python [package_name] && uv pip freeze --python ve/bin/python > requirements.txt` |
