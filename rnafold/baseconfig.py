from pathlib import Path
from typing import Optional, Type, TypeVar

import yaml
from pydantic import BaseModel

T = TypeVar("T", bound="BaseConfig")


class ConfigError(Exception):
    pass


class BaseConfig(BaseModel):
    """
    Base class for loading and managing configuration.
    Other config classes can extend this base class to add specific fields.
    """

    @classmethod
    def from_file_or_cli(cls: Type[T], config_path: Optional[Path], **cli_kwargs) -> T:
        """
        Load configuration from a YAML file if provided, or from cli arguments and
        validate it.
        """
        if config_path is not None:
            try:
                return cls.load_from_yaml(config_path)
            except (FileNotFoundError, yaml.YAMLError) as e:
                raise ConfigError(f"Failed to load config from {config_path}: {e}")

        return cls(**cli_kwargs)

    @classmethod
    def load_from_yaml(cls: Type[T], yaml_path: Path) -> T:
        """
        Load configuration from a YAML file and validate it.
        """
        try:
            with open(yaml_path, "r") as f:
                config_data = yaml.safe_load(f)
        except Exception as e:
            raise ConfigError(f"Error reading YAML config {yaml_path}: {e}")

        return cls(**config_data)
