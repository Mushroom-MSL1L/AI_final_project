import os
import sys

from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from llama_cpp import Llama
import pickle

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'DB')))
from db import db

# llama.cpp/llama-2-7b-chat.Q5_K_M.gguf accepts max 512 tokens
# llama.cpp-python constructor and call method: 
# https://note.com/npaka/n/n0ad63134fbe2#b9c86362-8a19-424d-b6ec-fddb7aba5de7
# https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.llama.Llama.create_completion
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
            #n_gpu_layers=-1,   #Use GPU acceleration
            verbose=True,       #output 
        )
        
        self.cache_path = "cache.pkl"
        self.cache = {}
        self.set_cache_path()
        self.load_cache()

    def __call__(self, question):
        return self.template_output(question)
    
    def set_cache_path(self):
        if not os.path.exists(self.cache_path):
            self.save_cache()

    def load_cache(self):
        with open(self.cache_path, 'rb') as f:
            self.cache = pickle.load(f)
        
    def save_cache(self):
        with open(self.cache_path, 'wb') as f:
            pickle.dump(self.cache, f)
    
    def reset_cachefile(self):
        self.cache = {}
        self.save_cache()
    
    def prompt_template(self, question):
        template = PromptTemplate.from_template(
            """
            Question: {question}
            Response:
            """
        )
        template = template.format(question=question)
        return template
    
    def raw_output(self, question):
        response = self.llm(prompt=question)

        return response["choices"][0]["text"]
    
    def template_output(self, question):
        question = self.prompt_template(question)
        response = self.llm(question)["choices"][0]["text"]
        return response

    def cache_output(self, question):
        question = self.prompt_template(question)
        if question in self.cache:
            print("Using cached response")
            return self.cache[question]
        else:
            response = self.llm(question)["choices"][0]["text"]
            self.cache[question] = response
            self.save_cache() 
            return response 
        
    
class Chain:
    def __init__(self):
        self.llm = LLM()
        self.db = db()
        self.name = None
        self.document = None
        self.prompt = None

    def __call__(self, name):
        self.name = name
        self.db.add_reviews()
        self.document = self.set_document()
        self.prompt = self.set_prompt()
        output = self.llm.cache_output(self.get_prompt())
        return output

    def db_add_reviews(self):
        #self.db.add_reviews(getName())
        raise NotImplementedError

    def get_name(self):
        return self.name
    
    def get_document(self):
        return self.document

    def get_prompt(self):
        return self.prompt

    def set_document(self):
        '''
        # forza horizon 4 reviews for testing
        document = {
            "Forces you to watch a one Minute commercial for all the DLCs before you can play it. That should be illegal. Ew.",
            "This game is a beautiful experience. As driving games go, it’s the best I’ve ever played, not only because of its irresistible scenery, exhilarating driving and perfectly-recreated cars, but because spending time with it puts me in a lasting good mood. It is uncomplicated and thrilling escapism in a shared driving",
            "It's a Shut up and take my money situation. This game is a party. Kept me smiling. When you don't do anything unique and new, you better do everything great. Forza Horizon series does everything as good as it gets. And in fairness, it does do some new things. It's an excellent, beautiful, smooth experience. As a side note, I liked the educational missions like Top Gear and British Racing Green story lines. Just lovely! Same goes for crossover missions like Halo and CP77. Please more! It's rare that a AAA game, feels like a labor of love. Double so when we are talking about a racing game.",
        }
        '''
        document = self.db.get_query_text(get_name(), 'fun game', n=5) # need to implement suitable keyword
        return document

    def set_prompt(self):
        # Define the prompt template for the model        
        template = PromptTemplate.from_template(
            """You are a helpful AI assistant.
            If you don't know the answer to a question, don't share false information.
            Your answer should be based on the context provided, game review of {name}.
            Your response should start with "{name} is", and end with ".", no other punctuation is allowed.

            Context: {context}

            Question: How would you describe {name}?
            """
        )
        prompt = template.format(context=self.get_document(), name=self.get_name())
        return prompt

#test LLM
prompt = "The quick brown fox" # output should be "jumps over the lazy dog"
testModel = LLM()
response = testModel(prompt)
print(response) 

#test Chain
#testChain = Chain()
#response = testChain("Forza Horizon 4")
#print(response)