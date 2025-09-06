from datetime import datetime
from fastapi import UploadFile
from langchain.embeddings.base import Embeddings
from langchain_chroma import Chroma
from transformers import ViTFeatureExtractor
from typing import List
from PIL import Image
from sentence_transformers import SentenceTransformer
import os
import shutil
import uuid

class CLIPEmbeddings(Embeddings):
    def __init__(self, model_name="clip-ViT-B-32"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, images):
        # Recebe lista de caminhos ou objetos PIL
        embeddings = []
        for img in images:
            if isinstance(img, str):
                img = Image.open(img)
            embeddings.append(self.model.encode([img])[0].tolist())
        return embeddings

    def embed_query(self, image):
        # Consulta (apenas 1 imagem)
        if isinstance(image, str):
            image = Image.open(image)
        return self.model.encode([image])[0].tolist()

class FaceReco(object):

    class SaveUserError(Exception):
        pass

    class VerifyUserError(Exception):
        pass

    def __init__(self):
        self.feature_extractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224-in21k')
        self.model = SentenceTransformer("clip-ViT-B-32")
        self.database_path = "./database/"
        self.vector_store = Chroma(
            collection_name="users",
            persist_directory="./database",
            embedding_function=CLIPEmbeddings()
        )
        self.embedding = CLIPEmbeddings()
        

    def register_user(self, files: List[UploadFile], username: str) -> bool:
        try:
            # Read all files and save your embeddings
            for file in files:
                local_temp_file = self.generate_temp_file(file)
                self.vector_store.add_texts(
                    texts=[local_temp_file],
                    metadatas=[{"user": username}],
                    embeddings=self.embedding.embed_query(local_temp_file)
                )
                os.remove(local_temp_file)
            return True
        except Exception as e:
            raise FaceReco.SaveUserError(f"Don't create the user!, because this error: {e}")
    
    def generate_temp_file(self, file: UploadFile) -> str:
        try:
            
            temp_dir = os.path.exists(self.database_path)
            if not temp_dir:
                os.makedirs("./database/", exist_ok=True)
            temp_dir = os.path.join(self.database_path)

            local_temp_file = os.path.join(temp_dir, f"{str(uuid.uuid4())}.jpg")
            with open(local_temp_file, "wb+") as temp_file:
                shutil.copyfileobj(file.file, temp_file)
            return local_temp_file
        except Exception as e:
            raise e
    
    def found_user(self, file: UploadFile):
        try:
            temp_file = self.generate_temp_file(file)
            query_embedding = self.embedding.embed_query(temp_file)
            
            results = self.vector_store.similarity_search_by_vector(
                query_embedding,
                k=3
            )

            if results:
                for info in results:
                    data = {
                        "msg": f"The user {info.metadata['user']} is authenticate!"
                    }
                    return data
            else:
                raise Exception({"msg": "User don't have access!"})
        except Exception as e:
             raise FaceReco.VerifyUserError(f"Don't found this user!, because this error: {e}")
    
    def embed_img(self, img_path: str):
        # Recebe lista de caminhos ou objetos PIL
        if isinstance(img_path, str):
            img_path = Image.open(img_path)
            return self.model.encode([img_path])[0].tolist()




        