from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA

class LLM:
    def __init__(self):
        self.model_path = "llama.cpp\llama-2-7b-chat.Q5_K_M.gguf"
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
        return self.llm.invoke(question)

class Model(LLM): #inherits from LLM
    def __init__(self, name, vector_store):
        super().__init__()
        self.name = name
        self.vector_store = vector_store
        self.model = setmodel()
    
    def getname(self):
        return self.name

    def prompt_template(self):
        # Define the prompt template for the model        
        template = """You are an helpful AI assistant. Your job is to answer the question sent by the user clearly, briefly and concisely.
        If you don't know the answer to a question, please don't share false information.

        Context: {context}
        Question: I want to know about the game {name}
        Response for Questions asked.
        Answer: 
        """

        template = PromptTemplate(
            template=template,
            input_variables=["context", "name"],
        )
        #template.format(name = self.name)
        return template
    
    def set_retriever(self):
        retriever = self.vector_store.as_retriever(search_kwargs={
            "k": 10, # number of documents to retrieve
            "filer": None,
            "namespace": getname(),
        }) 
        return retriever

    def setmodel(self):
        self.model = RetrievalQA.from_chain_type(
            retriever=self.set_retriever(),
            llm=self.llm,
            callback_manager=self.callback_manager,
            chaintype = "stuff", #Processing method of the searched text. other options: map_reduce,refine
            chain_type_kwargs={'prompt': prompt_template()},
            verbose=True,
        )
    
    def search(self, query):
        docs = set_retriever().invoke(query)
        return docs

    def output(self, name):
        template = prompt_template(name)
        return self.model.invoke(template)

testModel = LLM()
prompt = "tell me about National Yang-Ming Chiao Tung University, NYCU"
testModel.output(prompt)