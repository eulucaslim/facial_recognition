import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from deepface import DeepFace
from datetime import datetime
import cv2
import shutil


class FaceReco:

    class SaveUserError(Exception):
        pass

    class VerifyUserError(Exception):
        pass

    def __init__(self):
        self.users_folder = os.path.join("uploads/users")

    def register_user(self, img_bytes: bytes, user_name: str, cpf: str) -> True:
        try:
            # Create a past using the cpf user
            os.makedirs(self.users_folder, exist_ok=True)
            image_path = os.path.join(self.users_folder, f"{user_name}_{cpf}.jpg")

            # Save the user photo in server 
            with open(image_path, "wb+") as user_file:
                shutil.copyfileobj(img_bytes, user_file)

            return True
        except Exception as e:
            raise FaceReco.SaveUserError(f"Don't create the user!, because this error: {e}")
    
    def found_user(self, img_bytes: bytes):
        try:
            # Create the dir to temp files
            os.makedirs("temp", exist_ok=True)
            temp_file_path = os.path.join("temp", f"{datetime.now().strftime('%Y_%m_%d_%H_%M')}.jpg")

            # Write the temp_file
            with open(temp_file_path, "wb+") as temp_file:
                shutil.copyfileobj(img_bytes, temp_file)
            
            for files in os.listdir(self.users_folder):
                result = DeepFace.verify(
                    img1_path=temp_file_path, 
                    img2_path=os.path.join(self.users_folder, files)
                )
                if result['verified']:
                    print("Found The Image in Database")
            
            if result['verified'] == False:
                print("User don't have access!")
        except Exception as e:
             raise FaceReco.VerifyUserError(f"Don't found this user!, because this error: {e}")



        