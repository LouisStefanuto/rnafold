import os
from pathlib import Path

from pydantic import BaseModel, FilePath

from rnafold.baseconfig import BaseConfig

# Define the mapping of environments to config files
CONFIG_FILES = {
    "local": "config/global_local.yml",
    "kaggle": "config/global_kaggle.yml",
}


def get_config_file():
    """
    Returns the appropriate config file path based on the environment variable ENVIRONMENT.
    """
    env = os.getenv("ENVIRONMENT", "local")
    config_dir = Path(__file__).parent.parent

    if env in CONFIG_FILES:
        return config_dir / CONFIG_FILES[env]

    raise ValueError(
        f"Invalid ENVIRONMENT variable: '{env}'. Allowed values are: {', '.join(CONFIG_FILES.keys())}."
    )


class SequenceFiles(BaseModel):
    train: FilePath
    val: FilePath
    test: FilePath


class LabelsFiles(BaseModel):
    train: FilePath
    val: FilePath


class Files(BaseModel):
    sequences: SequenceFiles


class Tools(BaseModel):
    usalign: Path


class GlobalConfig(BaseConfig):
    sequences: SequenceFiles
    labels: LabelsFiles
    submission: FilePath
    tools: Tools


config_file = get_config_file()
Settings = GlobalConfig.load_from_yaml(config_file)
