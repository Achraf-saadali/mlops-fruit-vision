from huggingface_hub import login, upload_folder, snapshot_download
from dotenv import load_dotenv

import os


load_dotenv()

LOCAL_FOLDER_W = os.getenv("LOCAL_FOLDER_PATH_WINDOWS")


class HuggingFaceClient:

    def __init__(
        self,
        repo_id: str = "ACH-2003/food-inspection-mlops",
        local_folder: str = LOCAL_FOLDER_W
    ) -> None:
        print("Huggning" , LOCAL_FOLDER_W)
        self.local_folder = local_folder
        self.repo_id = repo_id

        login()


    def download(
        self,
        path_in_repo: str = "raw",
        repo_type: str = "dataset"
    ) -> None:

        snapshot_download(
            repo_id=self.repo_id,
            repo_type=repo_type,
            allow_patterns=f"LVIS_FRUITS_VEGETABLES/{path_in_repo}/**",
            local_dir=self.local_folder
        )

        print("Download via Hugging Face was successful.")


    def upload(
        self,
        path_in_repo: str = "raw",
        repo_type: str = "dataset"
    ) -> None:

        upload_folder(
            folder_path=self.local_folder,
            repo_id=self.repo_id,
            path_in_repo=F"LVIS_FRUITS_VEGETABLES/{path_in_repo}",
            repo_type=repo_type
        )

        print("Upload to Hugging Face was successful.")