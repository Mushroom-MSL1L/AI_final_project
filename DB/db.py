import os
import sys
import chromadb
from chromadb.utils import embedding_functions

from api import API
current_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, current_dir_path)

class db ():
    def __init__(self, 
                persistent_path=os.path.join(current_dir_path, 'data'), 
                collection_name='steam_reviews',
                embedding_func=embedding_functions.SentenceTransformerEmbeddingFunction()
                ):
        self.persistent_path = persistent_path
        self.collection_name = collection_name
        self.chroma_client = chromadb.PersistentClient(persistent_path)
        self.embedding_func = embedding_func
        self.collection = self.chroma_client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_func,
        )
        self.a = API()

    def add_reviews(self, game_name):
        game_id = self.a.get_game_Id(game_name)
        r = self.a.get_reviews(game_id)
        self.collection.add (
            ids=[str(game_id)+"_"+str(i) for i in range(len(r))],
            documents=r,
            metadatas=[{'game_id': game_id, 'game_name':game_name} for i in range(len(r))],
        )

    def get_query(self, game_name, query, n=5):
        return self.collection.query(
            where={'game_name': game_name},
            query_texts = query,
            n_results=n)
            
    def get_query_text(self, game_name, query, n=5):
        return self.get_query(game_name, query, n)['documents'][0]
    
    def get_query_by_embeddings(self, embeddings, n=5):
        return self.collection.query(
            query_embeddings=embeddings, 
            n_results=n)
    
    def get_collection(self):
        return self.collection()
    
# DB = db()
# DB.add_reviews('Forza Horizon 4')
# DB.add_reviews('Stardew Valley')
# print(DB.get_query_text('Forza Horizon 4', 'fun game', n=5))

