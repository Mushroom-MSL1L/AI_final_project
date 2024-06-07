from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain

import pickle
import os
import sys

# llama.cpp/llama-2-7b-chat.Q5_K_M.gguf accepts max 512 tokens
# llama.cpp-python constructor and call method: 
# https://api.python.langchain.com/en/latest/llms/langchain_community.llms.llamacpp.LlamaCpp.html#langchain_community.llms.llamacpp.LlamaCpp
class LLM:
    def __init__(self):
        self.model_path = r"Model/llama.cpp/llama-2-7b-chat.Q5_K_M.gguf"
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.model = LlamaCpp(
            #input include begging token + end token
            model_path=self.model_path,
            callback_manager=self.callback_manager,
            #n_gpu_layers=-1,   #Use GPU acceleration
            top_p=1,
            temperature=0.0,
            n_ctx=1024,         #context window, input length
            max_tokens=500,    #output length
            verbose=True,       #output 
        )
        
        self.cache_path = "cache.pkl"
        self.cache = {}
        self.set_cache_path()
        self.load_cache()

    def __call__(self, question):
        return self.raw_output(question)

    def set_nctx(self, n_ctx):
        self.model.n_ctx = n_ctx

    def set_max_tokens(self, max_tokens):
        self.model.max_tokens = max_tokens
    
    def set_cache_path(self):
        if not os.path.exists(self.cache_path):
            self.save_cache()
    
    def get_llm(self):
        return self.llm

    def load_cache(self):
        with open(self.cache_path, 'rb') as f:
            self.cache = pickle.load(f)
        
    def save_cache(self):
        with open(self.cache_path, 'wb') as f:
            if len(self.cache) > 100:
                self.cache.remove(self.cache[0])
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
        response = self.model.invoke(question)
        return response

    def gamechain_output(self, question, document, name):
        llm_chain = question | self.model
        response = llm_chain.invoke({"game_reviews": document, "name": name})
        return response
    
    def template_output(self, question):
        question = self.prompt_template(question)
        response = self.model.invoke(question)
        return response

    def cache_output(self, question):
        question = self.prompt_template(question)
        if question in self.cache:
            print("Using cached response")
            return self.cache[question]
        else:
            response = self.model.invoke(question)
            self.cache[question] = response
            self.save_cache() 
            return response

# llm = LLM()
# response = llm("What is the capital of France?")
# print(response)