from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain, StuffDocumentsChainr

from .model import LLM
from DB import db
from evaluation import TFIDF

class Chain:
    def __init__(self):
        self.llm = LLM()
        self.db = db()
        self.eval = None

    def __call__(self, name):
        # get reviews from db and set prompt for model
        
        self.update_db(name) # update db and add reviews

        document = self.set_document(name)
        prompt = self.set_prompt()
        result = self.output_chain(name, document, prompt)
        return result

    def update_db(self, name):
        # db size limit 10
        # add reviews if not in db

        game = self.db.get_DB_game_list()
        if len(game) > 10:
            self.db.delete_game(game[0])

        games = self.db.get_DB_game_list()
        if name not in games:
            self.db.add_reviews(name, n=1000)

    def get_length(self, documents):
        # get total length of documents

        total_length = 0
        for document in documents:
            for text in document:
                total_length += len(text)
        return total_length

    def set_document(self, name):
        # add reviews to document from db regarding to keywords
        # limit document length to 1000
        # return document as string

        keywords = ['size', 'graphic', 'gameplay', 'sound', 'target', 'storyline', 'difficulty', 'controls', 'player']
        documents = []
        str_docs = ''

        for keyword in keywords:
            document = self.db.get_query_text(name, keyword, n=20)
            documents.append(document)

        while self.get_length(documents) > 1000:
            for document in documents:
                document.pop(len(document)-1)

        for document in documents:
            for text in document:
                str_docs += text + ' '

        return str_docs

    def set_prompt(self):
        # Define the prompt template for the model        
        template = """ [INST] <<SYS>> Ensure that your response is informative and based on the reviews. <</SYS>>
            Reviews: {game_reviews}
            Prompt: Tell me about the game {name}. [/INST]
            """
        
        prompt = PromptTemplate(template=template, input_variables=['game_reviews', 'name'])
        return prompt
    
    def output_chain(self, name, document, prompt):
        # Define the chain of models to be used

        chain = prompt | self.llm.model
        result = chain.invoke({"game_reviews": document, "name": name})
        return result

    def test_chain():
        # test chain, not for practical use

        testChain = Chain()
        response = testChain("Forza Horizon 4")
        print("response: ", response)
        ### new edit ###
        reviews = testChain.db.get_game_all_reviews("Forza Horizon 4")
        tfidf = TFIDF()
        tfidf.load_data(reviews)
        print("score: ", tfidf.evaluate(response, n=1000))

#test LLM
# prompt = """You are a helpful AI assistant.
#         If you don't know the answer to a question, don't share false information.   
#         Your answer should be based on the context provided, game review of Forza Horizon 4.
#         Context: ['A fun game to play and I love how the cars are', 'I am hooked to this thing. It is fun. Can you believe that? A fun game?', 'its a fun multi and single player game with lots to do', 'Bought this game thinking that my friends who also bought it would play with me. Boy was I wrong. Fun game though will continue to be sad and play alone.', 'Wonderful game. If you are so done with your life this game can help you']
        
#         Question: Tell me about Forza Horizon 4."""
# print(len(prompt))
# testModel = LLM()
# response = testModel(prompt)
# print(response)

#test Chain
# testChain = Chain()
# response = testChain("Forza Horizon 4")
# print("response: ", response)

#test LLMChain
# llm = LLM()
#         template = """
#                 <s>[INST]<<SYS>>
#                 You are an AI assistant.
#                 Ensure that your response is informative and based on the provided reviews.
#                 <</SYS>>
#                 Reviews:{game_reviews}
#                 Prompt: Summarize the reviews for {name}.
#                 [/INST]
#                 """
#         prompt = PromptTemplate(template=template, input_variables=['game_reviews', 'name'])
#         #llm_chain = LLMChain(prompt=prompt, llm=llm.model) # if dictionary time needed
#         llm_chain = prompt | llm.model # if only string type output result needed
#         gamereviews = "['A fun game to play and I love how the cars are', 'I am hooked to this thing. It is fun. Can you believe that? A fun game?', 'its a fun multi and single player game with lots to do', 'Bought this game thinking that my friends who also bought it would play with me. Boy was I wrong. Fun game though will continue to be sad and play alone.', 'Wonderful game. If you are so done with your life this game can help you']"
#         result = llm_chain.invoke({"game_reviews": gamereviews, "name": "Forza Horizon 4"})
#         print("result: ")
#         print(result)