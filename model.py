from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import logging

class LLM:
    def __init__(self):
        self.model_path = r"llama.cpp/llama-2-7b-chat.Q5_K_M.gguf"
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = LlamaCpp(
            model_path=self.model_path,
            callback_manager=self.callback_manager,
            temperature=0.0,    #randomness
            n_ctx=512,
            n_batch=512,
            #max_tokens=512,    
            #n_gpu_layers=-1,   #Use GPU acceleration
            #stop={".", "!", "?"},  #stop token
            top_p=1,            #To increase the freedom of generated text, even when setting the temperature value high, adjusting the top_p parameter can help avoid text degradation.
            verbose=True,       #output 
        )

    def output(self, question):
        response = self.llm.invoke(question)
        return response #return self.llm(question)



class Chain(LLM): #inherits from LLM
    def __init__(self, name, vector_store):
        super.__init__()
        self.name = name
        self.vector_store = vector_store
        self.retriever = set_retriever()    
        self.chain = set_chain()

    def update(self, name):
        self.name = name
        self.retriever = set_retriever()    
        self.chain = set_chain()     

    def getName(self):
        return self.name

    def set_retriever(self):
        retriever = self.vector_store.as_retriever(search_kwargs={
            "k": 10,     # number of documents to retrieve
            "filer": None,
            "namespace": self.getName(),  #filter by name
        }) 
        return retriever

    def set_chain(self):
        return RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.set_retriever(),
            callback_manager=self.callback_manager,
            chaintype = "stuff",  #Processing method of the searched text. other options: map_reduce,refine
            chain_type_kwargs={'prompt': prompt_template()},
            verbose=True,
        )

    def set_prompt(self):
        # Define the prompt template for the model        
        template = """You are an helpful AI assistant. Your job is to answer the question sent by the user clearly, briefly and concisely.
        If you don't know the answer to a question, please don't share false information.
        Your answer to the question should be based on the context provided.

        Context: {context}
        Question: I want to know about the game {name} 
        Response for Questions asked.
        Answer: 
        """
        prompt = PromptTemplate(template, context=context, name=self.getName())
        return prompt

    def set_query(self):
        query = self.getName() + "game review" #search query for 
        return query

    def show_retrieval_result(self, response):
        for i, source in enumerate(response["source_documents"], 1):
            print(f"\nindex: {i}")
            print(f"{source.page_content}")

    def output(self, name):
        query = self.retrieval_query_template()
        response = self.chain.invoke(query)
        #self.show_retrieval_result(response)
        return response["result"]

if __name__ == "__main__":
    testModel = LLM()
    prompt = "capital of France?"
    testModel.output(prompt)