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
        self.cursor = self.chroma_client.get_or_create_collection(
            name='cursor',
            embedding_function=self.embedding_func,
        )
        self.a = API()

    def get_cursor(self, game_name):
        results = self.cursor.get(
            include=['metadatas', 'documents'],
        )
        for i in range(len(results['metadatas'])):
            if results['metadatas'][i]['game_name'] == game_name:
                return results['documents'][i]
        return '*'
    
    def set_or_update_cursor(self, game_name, cursor):
        r = self.get_cursor(game_name)
        if r == '*':
            self.cursor.add(
                ids=[game_name],
                documents=[cursor],
                metadatas=[{'game_name': game_name}],
            )
        else:
            self.cursor.update(
                ids=[game_name],
                documents=[cursor],
            )

    def add_reviews(self, game_name, n=100):
        game_id = self.a.get_game_Id(game_name)
        c = self.get_cursor(game_name)
        r, c = self.a.get_reviews(game_id=game_id, n=n, cursor=c,)
        self.set_or_update_cursor(game_name, c)
        offset = self.collection.count()
        self.collection.add (
            ids=[str(game_id)+"_"+str(offset+i) for i in range(len(r))],
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
    
    def get_game_review_number(self, game_name):
        results = self.collection.get(
            include=['metadatas'],
        )
        count = 0
        for r in results['metadatas']:
            if r['game_name'] == game_name:
                count += 1
        return count 
    
    def get_game_number(self):
        results = self.cursor.get(
            include=['metadatas'],
        )
        return len(results['metadatas'])
    
    def get_DB_game_list(self):
        results = self.cursor.get(
            include=['metadatas'],
        )
        return [r['game_name'] for r in results['metadatas']]
    
    def delete_game(self, game_name):
        is_deleted = False
        has_game = False
        results = self.collection.get(
            include=['metadatas'],
        )
        for r in results['metadatas']:
            if r['game_name'] == game_name : 
                has_game = True 
                break
        if has_game: 
            self.collection.delete(
                where={'game_name': game_name},
            )
            self.cursor.delete(
                where={'game_name': game_name},
            )
            is_deleted = True
        return is_deleted, has_game

### Example
# DB = db()
# DB.add_reviews('Forza Horizon 4')
# DB.add_reviews('Stardew Valley')
# print(DB.get_DB_game_list())
# print('query: ', DB.get_query_text('Forza Horizon 4', 'fun game', n=10))
# print('#(Forza Horizon 4): ', DB.get_game_review_number('Forza Horizon 4'))
# print('#(Stardew Valley): ', DB.get_game_review_number('Stardew Valley'))
# print('#', DB.get_game_number())
# DB.delete_game('Stardew Valley')
# print('#(Forza Horizon 4): ', DB.get_game_review_number('Forza Horizon 4'))
# print('#(Stardew Valley): ', DB.get_game_review_number('Stardew Valley'))
# print('#', DB.get_game_number())