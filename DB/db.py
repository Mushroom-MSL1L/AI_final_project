from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import LlamaCppEmbeddings
import sys
import os

from api import API
current_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir_path)

class db :
    def __init__(self, persistant_directory = os.path.join(current_dir_path, "data")) :
        self.project_root_path = os.path.dirname(current_dir_path)
        self.llama_model_path = os.path.join(self.project_root_path, "llama.cpp", "models", "llama-2-7b", "llama-2-7b-7B-F32-q4_0.gguf")
        self.persistant_directory = self.set_persistant_directory(persistant_directory)
        self.embeddings = LlamaCppEmbeddings(model_path=self.llama_model_path)
        self.chroma_db = Chroma(
                persist_directory=persistant_directory, 
                embedding_function=self.embeddings,
                collection_name="lc_chroma_demo")
        self.api = API()

    def set_persistant_directory(self, persistant_directory) :  
        if not os.path.exists(persistant_directory):
            os.makedirs(persistant_directory)
        return persistant_directory
    
    def add_reviews(self, game_name) :
        game_id = self.api.get_game_Id(game_name)
        r = self.api.get_reviews(game_id)
        self.chroma_db.add_texts(
            texts=r,
        )
        self.chroma_db.persist()

    def get_similar_texts (self, query, n=5) :
        return self.chroma_db.get_similar_texts(
            query=query,
            n=n
        )
    
# DB = db()
# DB.add_reviews("Forza Horizon 5")
# print(DB.get_similar_texts("I love the game", 5))
