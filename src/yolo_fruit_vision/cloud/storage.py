
from .huggingface_client import HuggingFaceClient





client_registry =  {

"Hugging_face" : HuggingFaceClient()




}


class Storage  :

    def __init__(self  ,choice : str = "Hugging_face" , local_folder :str = "")->None :

        self.client = client_registry.get(choice , None)

        self.choice = choice
        if self.client is None : 

            raise RuntimeError("No client  was attached")


        if local_folder != "":
            self.client.local_folder = local_folder




    def download(self , path_in_repo = "raw")->None  :

        self.client.download(path_in_repo = path_in_repo)


    # Choice of data Upload either at raw or processed or interim ...............
    def upload(self , path_in_repo : str = "raw")->None  :

        self.client.upload(path_in_repo = path_in_repo) 



    def __str__(self):

        return f"""choice : {self.choice}
Local folder : {self.client.local_folder}"""                




          

