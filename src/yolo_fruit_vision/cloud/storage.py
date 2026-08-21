"""Storage adapter used by the data-ingestion component."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from yolo_fruit_vision.cloud.huggingface_client import HuggingFaceClient
from yolo_fruit_vision.entity.config_entity import DataIngestionConfig


class Storage:
    """Map data-ingestion configuration to Hugging Face storage operations.

    ``config.root_dir`` is used only as a local download destination.
    An upload source is supplied explicitly because the original ACFR folder can
    live outside the MLOps repository.
    """

    def __init__(
        self,
        config: DataIngestionConfig,
        token: Optional[str] = None,
    ) -> None:
        self.config = config
        self.client = HuggingFaceClient(
            repo_id=config.repo_id,
            repo_type=config.repo_type,
            token=token,
            private=config.private,
        )

    def download(self) -> Path:
        """Download configured remote raw data into the local artifacts directory."""
        return self.client.download_folder(
            remote_dir=self.config.remote_dir,
            local_root=self.config.root_dir,
        )

    def upload(self, source_folder: Path, commit_message: str) -> str:
        """Upload an explicit local source folder to the configured remote raw path."""
        return self.client.upload_folder(
            local_folder=source_folder,
            path_in_repo=self.config.remote_dir,
            commit_message=commit_message,
        )
