from huggingface_hub import login, upload_folder, snapshot_download
from dotenv import load_dotenv
from yolo_fruit_vision import logger

import os





class HuggingFaceClient:

    def __init__(
        self,
        repo_id: str = "",
        local_folder: str = "" 
    ) -> None:
        load_dotenv()

        LOCAL_FOLDER_W = os.getenv("LOCAL_FOLDER_PATH_WINDOWS")

        REPO_ID_DETECTION = os.getenv("REPO_ID_DETECTION")

        if local_folder  == "":
            local_folder = LOCAL_FOLDER_W

        if repo_id == "":
            repo_id = REPO_ID_DETECTION

        self.local_folder = local_folder

        self.repo_id = repo_id

        self.path_in_repo = path_in_repo

        logger.info("Attempt to Login ...")
        login()
        logger.info("Sucessfull  Login ...")


    def download(
        self,
        path_in_repo: str = "",  # full path in repository
        repo_type: str = "dataset"
    ) -> None:

        snapshot_download(
            repo_id=self.repo_id,
            repo_type=repo_type,
            allow_patterns=f"{path_in_repo}/**",
            local_dir=self.local_folder
        )

        logger.info(f"Download via Hugging Face was successful of folder :{path_in_repo}")


    def upload(
        self,
        path_in_repo: str = "", # full path in repository
        repo_type: str = "dataset"
    ) -> None:

        upload_folder(
            folder_path=self.local_folder,
            repo_id=self.repo_id,
            path_in_repo=f"{path_in_repo}",
            repo_type=repo_type
        )

        logger.info("Upload to Hugging Face was successful.")


    def __str__(self):

        return f'''
    repository_id = {self.repo_id}
    local_folder = {self.local_folder}
'''    