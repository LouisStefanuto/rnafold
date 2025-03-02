import pathlib

import yaml
from pydantic import BaseModel

cwd = pathlib.Path(__file__).parent
config_file = cwd / "config.yml"


class SequenceFiles(BaseModel):
    train: str
    val: str
    test: str


class LabelsFiles(BaseModel):
    train: str
    val: str


class Files(BaseModel):
    sequences: SequenceFiles


class Tools(BaseModel):
    usalign: str


class Config(BaseModel):
    sequences: SequenceFiles
    labels: LabelsFiles
    submission: str
    tools: Tools


def _load_yml_config(path: pathlib.Path):
    """Classmethod returns YAML config"""
    try:
        return yaml.safe_load(path.read_text())

    except FileNotFoundError as error:
        message = "Error: yml config file not found."
        raise FileNotFoundError(error, message) from error


Settings = Config(**_load_yml_config(config_file))
