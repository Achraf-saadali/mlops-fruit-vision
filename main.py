"""Command entry point for the MLOps Fruit Vision pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from yolo_fruit_vision.pipeline.stage01_data_ingestion import DataIngestionPipeline


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env")


def build_parser() -> argparse.ArgumentParser:
    """Build the Stage 01 command-line interface."""
    parser = argparse.ArgumentParser(
        description="Stage 01: preserve and transfer the original ACFR raw dataset."
    )
    parser.add_argument(
        "action",
        choices=("upload", "download"),
        help="'upload' sends untouched local ACFR data to Hugging Face; "
        "'download' retrieves raw data into artifacts/.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        help=(
            "Required for upload. Path to the extracted folder named "
            "'acfr-fruit-dataset'."
        ),
    )
    return parser


def main() -> None:
    """Run one Stage 01 action."""
    args = build_parser().parse_args()
    pipeline = DataIngestionPipeline()

    if args.action == "upload":
        if args.source is None:
            raise SystemExit(
                "Upload requires --source. Example:\n"
                'python main.py upload --source "C:\\path\\to\\acfr-fruit-dataset"'
            )

        result = pipeline.upload(source_folder=args.source)
        print(json.dumps(result, indent=2))
        return

    local_data_dir = pipeline.download()
    print(f"Download completed: {local_data_dir}")


if __name__ == "__main__":
    main()
