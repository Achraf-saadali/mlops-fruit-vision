
from .huggingface_client import HuggingFaceClient

from yolo_fruit_vision import logger



client_registry =  {

"Hugging_face" : HuggingFaceClient()




}


class Storage  :

    def __init__(self  ,choice : str = "Hugging_face" , local_folder :str = "",repo_id :str = "")->None :

        self.client = client_registry["Hugging_face"]
        self.choice = choice

        if local_folder != "":
            self.client.local_folder = local_folder

        if repo_id != "":
            self.client.repo_id = repo_id   






    def download(self , path_in_repo = "")->None  :
        if path_in_repo == "":
            logger.fatal(f"Unsuccessfull download : No repository was specified")
            return None
        self.client.download(path_in_repo = path_in_repo)


    # Choice of data Upload either at raw or processed or interim ...............
    def upload(self , path_in_repo : str = "")->None  :

        if path_in_repo == "":
                logger.fatal(f"Unsuccessfull upload : No repository was specified")
                return None
                

        self.client.upload(path_in_repo = path_in_repo) 



    def __str__(self):

         return  f'''
client = {self.choice}
metadata = {self.client}
'''                




          

