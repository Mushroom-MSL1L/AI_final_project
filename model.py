import os
import sys

from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from llama_cpp import Llama
import pickle

from DB.db import DB

class LLM:
    def __init__(self):
        self.model_path = r"llama.cpp/llama-2-7b-chat.Q5_K_M.gguf"
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = Llama(
            model_path=self.model_path,
            callback_manager=self.callback_manager,
            temperature=0.0,    #randomness
            n_ctx=512, 
            n_batch=512,
            #max_tokens=512,    
            #n_gpu_layers=-1,   #Use GPU acceleration
            stop = ["."],  #stop token
            top_p=1,            #To increase the freedom of generated text, even when setting the temperature value high, adjusting the top_p parameter can help avoid text degradation.
            verbose=True,       #output 
        )
  
        self.cache_path = "cache.pkl"
        self.cache = {}
        self.set_cache_path()
        self.load_cache()
    
    def set_cache_path(self):
        if not os.path.exists(self.cache_path):
            self.save_cache()

    def load_cache(self):
        with open(self.cache_path, 'rb') as f:
            self.cache = pickle.load(f)
        
    def save_cache(self):
        with open(self.cache_path, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def prompt_template(self, question):
        template = PromptTemplate.from_template(
            "Question: {question}"
        )
        template = template.format(question=question)
        return template
    
    def output(self, question):
        question = self.prompt_template(question)
        response = self.llm(question)["choices"][0]["text"]
        print(response)

    def output_cache(self, question):
        question = self.prompt_template(question)
        if question in self.cache:
            print("Using cached response")
            print(self.cache[question])
        else:
            response = self.llm(question)["choices"][0]["text"]
            self.cache[question] = response
            print(response)
            self.save_cache()  
        
    
class Chain(LLM): #inherits from LLM
    def __init__(self, name, vector_store):
        super().__init__()

        self.db = db.DB()
        self.name = set_name(name)  
        self.document = get_document()
        self.prompt = set_prompt()
        db.add_reviews(getName())

    def update(self, name):
        self.name = set_name(name)
        self.db_add_reviews()
        self.document = set_document()
        self.prompt = set_prompt()

    def db_add_reviews(self):
        self.db.add_reviews(getName())

    def getName(self):
        return self.name
    
    def get_document(self):
        return self.document

    def get_prompt(self):
        return self.prompt

    def set_name(self, name):
        self.name = name

    def set_document(self):
        document = self.db.get_query_text(getName(), 'fun game', n=5)
        return document

    def set_prompt(self, context):
        # Define the prompt template for the model        
        template = PromptTemplate(
        """You are an helpful AI assistant. Your job is to answer the question sent by the user clearly, briefly and concisely.
        If you don't know the answer to a question, please don't share false information.
        Your answer to the question should be based on the context provided.

        Context: {context}
        Question: I want to know about the game {name} 
        Response for Questions asked.
        Answer: """
        )
        self.prompt = template.format(template, context=context, name=self.getName())

    def output(self, name):
        self.update(name)
        response = self.llm.output_cache(prompt)
        return response

if __name__ == "__main__":
    #test LLM
    #testModel = LLM()
    #prompt = "What is the color of the sky?"
    #testModel.output_cache(prompt)
    
    # test Chain
    testChain = Chain("")
    