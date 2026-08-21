"""Stage 01 pipeline runner for raw ACFR data ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from yolo_fruit_vision.components.data_ingestion import DataIngestion
from yolo_fruit_vision.config.configuration import ConfigurationManager


class DataIngestionPipeline:
    """Connect Stage 01 configuration and raw ACFR ingestion logic."""

    def __init__(self) -> None:
        config = ConfigurationManager().get_data_ingestion_config()
        self.ingestion = DataIngestion(config=config)

    def upload(self, source_folder: str | Path) -> Dict[str, Any]:
        """Validate and upload the original ACFR root without modifying it."""
        return self.ingestion.upload_data(source_folder=source_folder)

    def download(self) -> Path:
        """Download the original ACFR raw folder to local artifacts."""
        return self.ingestion.download_data()
