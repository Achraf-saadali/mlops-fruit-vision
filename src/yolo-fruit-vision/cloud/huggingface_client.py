from huggingface_hub import login, upload_folder

# (optional) Login with my Hugging Face credentials
login()

# Pushing my dataset files
upload_folder(folder_path="C:\Users\achra\Downloads\LVIS_Fruits_And_Vegetables", repo_id="ACH-2003/food-inspection-mlops", repo_type="dataset")
