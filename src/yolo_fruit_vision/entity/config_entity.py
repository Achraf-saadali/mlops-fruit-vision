from dataclasses import dataclass
from pathlib import Path
from typing import Tuple


@dataclass(frozen=True)
class DataIngestionConfig:
    """Settings needed by the raw ACFR data-ingestion stage."""

    root_dir: Path
    repo_id: str
    repo_type: str
    remote_dir: str
    private: bool
    expected_fruit_folders: Tuple[str, ...] = ("almonds", "apples", "mangoes")

    @property
    def local_data_dir(self) -> Path:
        """The local artifact folder corresponding to the configured remote path."""
        return self.root_dir / self.remote_dir
