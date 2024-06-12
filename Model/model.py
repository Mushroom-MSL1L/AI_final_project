from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_fireworks import Fireworks
from langchain.callbacks.base import BaseCallbackHandler

import pickle
import torch
import os
import sys

# llama.cpp-python constructor and call method: 
# https://api.python.langchain.com/en/latest/llms/langchain_community.llms.llamacpp.LlamaCpp.html#langchain_community.llms.llamacpp.LlamaCpp

class LLM:
    def __init__(self):
        self.device = {
            "gpu": True if torch.cuda.is_available() else False,
        }

        self.config = {
            "max_tokens": 1024, # output terminates as the model reaches the max token
            "n_ctx": 4096 if self.device['gpu'] else 1024, # context window, input length
            "n_batch": 512 if self.device['gpu'] else 8, # batch size
            "n_gpu_layers": -1 if self.device['gpu'] else None, # number of layers
        }

        self.model_path = r"Model/llama.cpp/llama-2-7b-chat.Q4_K_M.gguf"

        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        self.model = LlamaCpp(
            #begining token + end token counted as 2 tokens in the input
            model_path=self.model_path,
            callback_manager=self.callback_manager,     #log outputs
            n_ctx=self.config['n_ctx'],                 #context window, input length
            max_tokens=self.config['max_tokens'],       #output length
            n_gpu_layers=self.config['n_gpu_layers'],   #number of layers             
            n_batch=self.config['n_batch'],
            verbose=True,                               #output
            top_p=1,                                    #prevent model from generating low probability tokens  
            top_k=40,                                   #top k tokens for next token prediction    
            temparature = 0.0,                          #temparature for sampling
        )

        self.cache_path = "Model/cache.pkl"
        self.cache = {}
        self.set_cache_path()
        self.load_cache()

    def __call__(self, question, prompt, document, name):
        return self.game_output(question=question, prompt=prompt, document=document, name=name)
    
    def fireworks(self, prompt):
        bot = Fireworks(
            model="accounts/fireworks/models/llama-v3-70b-instruct", # model path in the server
            max_tokens=512,
        )
        response = bot(prompt)
        return response

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
            if len(self.cache) > 1000:
                self.cache.remove(next(iter(self.cache)))
            pickle.dump(self.cache, f)
    
    def reset_cachefile(self):
        self.cache = {}
        self.save_cache()
    
    def prompt_template(self, question):
        template = PromptTemplate.from_template(
            """
            <s> [INST] <<SYS>> You are a helpful AI assistant. <</SYS>>
            Question: {question}
            Response:
            [/INST]
            """
        )
        template = template.format(question=question)
        return template
    
    def raw_output(self, question):
        response = self.model.invoke(question)
        return response

    def template_output(self, question):
        question = self.prompt_template(question)
        response = self.model.invoke(question)
        return response

    def cache_output(self, question):
        question = self.prompt_template(question)
        if question in self.cache:
            return self.cache[question]
        else:
            response = self.model.invoke(question)
            self.cache[question] = response
            self.save_cache() 
            return response
    
    def game_output(self, question, prompt, document, name):
        if question in self.cache:
            return self.cache[question]
        else:
            chain = prompt | self.model
            response = chain.invoke({"game_reviews": document, "name": name})
            self.cache[question] = response
            self.save_cache() 
            return response

# llm = LLM()
# response = llm("What is the capital of France?")
# print(response)