from huggingface_hub import login, upload_folder


def main()->None:
    # Uploading data to my  cloud storage at hugging face 
    upload_data()







    return None




def upload_data()->None  :
    # (optional) Login with my Hugging Face credentials
    login()

    # Pushing my dataset files
    upload_folder(folder_path=r"C:\Users\achra\Downloads\LVIS_Fruits_And_Vegetables", repo_id="ACH-2003/food-inspection-mlops", repo_type="dataset")

    return None



































if __name__ == '__main__':
    main()