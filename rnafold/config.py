import os
import pathlib

import yaml
from pydantic import BaseModel

# Define the mapping of environments to config files
CONFIG_FILES = {
    "local": "config_local.yml",
    "kaggle": "config_kaggle.yml",
}


def get_config_file():
    """
    Returns the appropriate config file path based on the environment variable ENVIRONMENT.
    """
    env = os.getenv("ENVIRONMENT", "local")
    config_dir = pathlib.Path(__file__).parent.parent / "config"

    if env in CONFIG_FILES:
        return config_dir / CONFIG_FILES[env]

    raise ValueError(
        f"Invalid ENVIRONMENT variable: '{env}'. Allowed values are: {', '.join(CONFIG_FILES.keys())}."
    )


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


config_file = get_config_file()
Settings = Config(**_load_yml_config(config_file))
