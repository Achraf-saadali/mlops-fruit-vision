"""Configuration loading for pipeline stages."""

from pathlib import Path

from yolo_fruit_vision.entity.config_entity import DataIngestionConfig
from yolo_fruit_vision.utils.common import read_yaml


# Works on Windows, Colab, and Linux because it is calculated from this file.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "config.yaml"


class ConfigurationManager:
    """Read YAML settings and build typed configuration objects."""

    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
        self.config_path = Path(config_path)
        self.config = read_yaml(path_to_yaml=self.config_path)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """Return the settings for Stage 01: raw ACFR data ingestion."""
        if "data_ingestion" not in self.config:
            raise KeyError("Missing 'data_ingestion' section in config/config.yaml")

        section = self.config["data_ingestion"]
        required = {"root_dir", "repo_id", "repo_type", "remote_dir"}
        missing = required - set(section.keys())
        if missing:
            raise KeyError(
                f"Missing data_ingestion settings: {', '.join(sorted(missing))}"
            )

        root_dir = Path(section["root_dir"])
        if not root_dir.is_absolute():
            root_dir = PROJECT_ROOT / root_dir

        expected_fruit_folders = tuple(
            section.get("expected_fruit_folders", ["almonds", "apples", "mangoes"])
        )

        return DataIngestionConfig(
            root_dir=root_dir,
            repo_id=section["repo_id"],
            repo_type=section["repo_type"],
            remote_dir=section["remote_dir"].strip("/"),
            private=section.get("private", True),
            expected_fruit_folders=expected_fruit_folders,
        )
