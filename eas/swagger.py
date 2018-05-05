import pathlib


with open(pathlib.Path(__file__).parent / "swagger.yaml") as f:
    YAML_DEFINITION = f.read()

