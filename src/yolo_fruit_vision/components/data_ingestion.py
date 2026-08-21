"""Stage 01: preserve and move the original ACFR multi-fruit dataset."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

from yolo_fruit_vision import logger
from yolo_fruit_vision.cloud.storage import Storage
from yolo_fruit_vision.entity.config_entity import DataIngestionConfig


class DataIngestion:
    """Validate, upload, and download raw ACFR data without changing annotations.

    This stage never creates YOLO labels. ACFR circles, rectangles, CSV files, set
    files, and Apple segmentations are preserved exactly as provided.
    """

    REQUIRED_FRUIT_ITEMS = ("images", "annotations", "sets", "labelmap.json")
    REQUIRED_SPLIT_FILES = ("all.txt", "train.txt", "val.txt", "test.txt")

    def __init__(self, config: DataIngestionConfig) -> None:
        self.config = config

    def _storage(self) -> Storage:
        """Build storage with a token if the current runtime provides one."""
        return Storage(config=self.config, token=os.getenv("HF_TOKEN"))

    def inspect_raw_acfr_dataset(self, source_folder: str | Path) -> Dict[str, Any]:
        """Validate the documented ACFR layout and return a compact inventory."""
        source_folder = Path(source_folder).expanduser().resolve()

        if not source_folder.is_dir():
            raise FileNotFoundError(
                f"ACFR source folder does not exist: {source_folder}\n"
                "Extract the zip file first, then pass the real 'acfr-fruit-dataset' "
                "directory—not a path displayed inside a .zip archive."
            )

        if source_folder.name != "acfr-fruit-dataset":
            raise ValueError(
                "The source folder must be the extracted ACFR dataset root named "
                f"'acfr-fruit-dataset', not its parent directory: {source_folder}"
            )

        readme_path = source_folder / "readme.txt"
        if not readme_path.is_file():
            raise FileNotFoundError(f"Missing required ACFR readme: {readme_path}")

        summary: Dict[str, Any] = {
            "dataset_root": str(source_folder),
            "readme": str(readme_path),
            "fruit_subsets": {},
        }

        for fruit_name in self.config.expected_fruit_folders:
            fruit_dir = source_folder / fruit_name
            if not fruit_dir.is_dir():
                raise FileNotFoundError(f"Missing ACFR fruit folder: {fruit_dir}")

            missing_items = [
                name for name in self.REQUIRED_FRUIT_ITEMS
                if not (fruit_dir / name).exists()
            ]
            if missing_items:
                raise FileNotFoundError(
                    f"ACFR subset '{fruit_name}' is incomplete. Missing: "
                    f"{', '.join(missing_items)}"
                )

            missing_splits = [
                name for name in self.REQUIRED_SPLIT_FILES
                if not (fruit_dir / "sets" / name).is_file()
            ]
            if missing_splits:
                raise FileNotFoundError(
                    f"ACFR subset '{fruit_name}' has missing split files: "
                    f"{', '.join(missing_splits)}"
                )

            images = list((fruit_dir / "images").glob("*.png"))
            annotations = list((fruit_dir / "annotations").glob("*.csv"))

            summary["fruit_subsets"][fruit_name] = {
                "image_count": len(images),
                "annotation_csv_count": len(annotations),
                "has_segmentation": (fruit_dir / "segmentations").is_dir(),
                "split_files": list(self.REQUIRED_SPLIT_FILES),
                "annotation_geometry": (
                    "circle" if fruit_name == "apples" else "rectangle"
                ),
            }

        return summary

    def upload_data(self, source_folder: str | Path) -> Dict[str, Any]:
        """Upload the untouched extracted ACFR root to Hugging Face once."""
        summary = self.inspect_raw_acfr_dataset(source_folder)
        source_folder = Path(source_folder).expanduser().resolve()

        commit_oid = self._storage().upload(
            source_folder=source_folder,
            commit_message="Upload original ACFR multi-fruit 2016 raw dataset",
        )

        summary["huggingface_repo_id"] = self.config.repo_id
        summary["huggingface_remote_dir"] = self.config.remote_dir
        summary["commit_oid"] = commit_oid

        logger.info(
            "Raw ACFR ingestion upload completed: %s → %s/%s",
            source_folder,
            self.config.repo_id,
            self.config.remote_dir,
        )
        return summary

    def download_data(self) -> Path:
        """Download the configured untouched ACFR raw folder to local artifacts."""
        local_data_dir = self._storage().download()
        logger.info("Raw ACFR ingestion download completed: %s", local_data_dir)
        return local_data_dir
