"""Low-level Hugging Face Dataset repository operations."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from huggingface_hub import HfApi, snapshot_download

from yolo_fruit_vision import logger


class HuggingFaceClient:
    """Upload and download folders from one Hugging Face Hub repository.

    This class deliberately does not load ``.env`` or call ``login()``. The caller
    provides an optional token at runtime. That keeps importing this module safe in
    local development, Colab, and CI environments.
    """

    def __init__(
        self,
        repo_id: str,
        repo_type: str = "dataset",
        token: Optional[str] = None,
        private: bool = False,
    ) -> None:
        if not repo_id:
            raise ValueError("repo_id must not be empty.")

        self.repo_id = repo_id
        self.repo_type = repo_type
        self.token = token
        self.private = private
        self.api = HfApi(token=token)

    def download_folder(self, remote_dir: str, local_root: Path) -> Path:
        """Download one remote folder beneath a local root directory.

        Public repositories may be downloaded without a token. A private repository
        requires an ``HF_TOKEN`` with read access.
        """
        remote_dir = remote_dir.strip("/")
        if not remote_dir:
            raise ValueError("remote_dir must not be empty.")

        local_root = Path(local_root)
        local_root.mkdir(parents=True, exist_ok=True)

        logger.info(
            "Downloading '%s' from %s into %s",
            remote_dir,
            self.repo_id,
            local_root,
        )

        snapshot_download(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            allow_patterns=[f"{remote_dir}/**"],
            local_dir=str(local_root),
            token=self.token,
        )

        local_data_dir = local_root / remote_dir
        if not local_data_dir.is_dir():
            raise FileNotFoundError(
                "The download finished, but the expected folder was not found: "
                f"{local_data_dir}. Check repo_id and remote_dir in config.yaml."
            )

        logger.info("Hugging Face download completed: %s", local_data_dir)
        return local_data_dir

    def upload_folder(
        self,
        local_folder: Path,
        path_in_repo: str,
        commit_message: str,
    ) -> str:
        """Upload a local folder to a remote folder and return commit information.

        Creating or modifying a Hub repository always requires an authenticated token
        with write access.
        """
        if not self.token:
            raise ValueError(
                "HF_TOKEN is required for upload. Add a write token to .env locally "
                "or set it as a Colab Secret/environment variable."
            )

        local_folder = Path(local_folder)
        path_in_repo = path_in_repo.strip("/")

        if not local_folder.is_dir():
            raise FileNotFoundError(f"Local upload folder does not exist: {local_folder}")
        if not path_in_repo:
            raise ValueError("path_in_repo must not be empty.")

        # This creates the repository only when it does not already exist.
        self.api.create_repo(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            private=self.private,
            exist_ok=True,
        )

        logger.info(
            "Uploading %s to %s/%s",
            local_folder,
            self.repo_id,
            path_in_repo,
        )

        commit_info = self.api.upload_folder(
            repo_id=self.repo_id,
            repo_type=self.repo_type,
            folder_path=str(local_folder),
            path_in_repo=path_in_repo,
            commit_message=commit_message,
            ignore_patterns=[
                "**/__pycache__/**",
                "**/*.pyc",
                "**/.cache/**",
                "**/.DS_Store",
            ],
        )

        logger.info("Hugging Face upload completed: %s", commit_info.oid)
        return str(commit_info.oid)
