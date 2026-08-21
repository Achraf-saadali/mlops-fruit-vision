from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    """Settings needed by the data-ingestion stage."""

    root_dir: Path
    repo_id: str
    repo_type: str
    remote_dir: str
    private: bool

    @property
    def local_data_dir(self) -> Path:
        """The local folder corresponding to remote_dir."""
        return self.root_dir / self.remote_dir