from pathlib import Path
from unittest.mock import mock_open, patch

import pytest
import yaml
from pydantic import ValidationError

from rnafold.baseconfig import BaseConfig


class ExampleConfig(BaseConfig):
    param1: str
    param2: int


@pytest.fixture
def valid_yaml_data():
    return {"param1": "value1", "param2": 42}


class TestBaseConfig:
    def test_init_with_args(self):
        config = ExampleConfig(param1="value1", param2=42)
        assert config.param1 == "value1"
        assert config.param2 == 42

    def test_init_with_dict(self):
        data = {"param1": "value1", "param2": 42}
        config = ExampleConfig(**data)
        assert config.param1 == "value1"
        assert config.param2 == 42

    @patch(
        "builtins.open", new_callable=mock_open, read_data="param1: value1\nparam2: 42"
    )
    @patch("yaml.safe_load", return_value={"param1": "value1", "param2": 42})
    def test_load_from_yaml_valid(self, mock_safe_load, mock_file):
        # Given: Mocked open and safe_load behavior
        yaml_path = Path("fake_config.yaml")

        # When: Calling load_from_yaml with mocked YAML path
        config = ExampleConfig.load_from_yaml(yaml_path)

        # Then: Validate the content loaded is as expected
        assert config.param1 == "value1"
        assert config.param2 == 42

        mock_file.assert_called_once_with(yaml_path, "r")
        mock_safe_load.assert_called_once()

    # Invalid field3, missing field 2
    @patch(
        "builtins.open", new_callable=mock_open, read_data="param1: value1\nfield3: 42"
    )
    @patch("yaml.safe_load", return_value={"param1": "value1", "field3": 999})
    def test_load_from_yaml_invalid(self, mock_safe_load, mock_file):
        # Given: Mocked open and safe_load behavior
        yaml_path = Path("fake_config.yaml")

        # When: Calling load_from_yaml with mocked YAML path
        with pytest.raises(ValidationError):
            _ = ExampleConfig.load_from_yaml(yaml_path)

        mock_file.assert_called_once_with(yaml_path, "r")
        mock_safe_load.assert_called_once()

    def test_from_file(self, valid_yaml_data, tmp_path):
        """
        Test that from_file_or_cli correctly loads config from a valid YAML file.
        """
        # Create a temporary YAML file with valid data
        yaml_file = tmp_path / "config.yaml"
        with open(yaml_file, "w") as f:
            yaml.dump(valid_yaml_data, f)

        # Call the method with the config path
        config = ExampleConfig.from_file_or_cli(config_path=yaml_file)

        # Assert that the loaded config matches the expected values
        assert config.param1 == "value1"
        assert config.param2 == 42

    def test_from_cli(self, valid_yaml_data):
        """
        Test that from_file_or_cli correctly loads config from CLI kwargs.
        """
        # Simulate CLI arguments by passing them directly as kwargs
        config = ExampleConfig.from_file_or_cli(config_path=None, **valid_yaml_data)

        # Assert that the loaded config matches the expected values
        assert config.param1 == "value1"
        assert config.param2 == 42
