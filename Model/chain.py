from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

from .model import LLM
from DB import db

class Chain:
    def __init__(self):
        self.llm = LLM()
        self.db = db()
        self.eval = None
        self.config = {}

        self.config = {
            "keywords": ['size', 'graphic', 'gameplay', 'sound', 'target',
                         'storyline', 'difficulty', 'controls', 'price', 'player'],
            "total_document_length": 3800 if self.llm.device['gpu'] else 900,
            "add_review_number": 1000, 
            "max_docs_length": 300 if self.llm.device['gpu'] else 90,
        }

    def __call__(self, name):
        # get reviews from db and set prompt for model
        enoughreview, id =  self.update_db(name) # update db and add reviews
        template, prompt = self.set_prompt()
        str_docs, list_docs = self.set_document(name)
        result = self.output_chain(name, id, enoughreview, str_docs, template, prompt)
        return result

    def update_db(self, name):
        # db size limit 10
        # add reviews if reviews for the game not in db or less than 100
        # return True if reviews are enough
        # return False if reviews are not enough

        noID = None

        game = self.db.get_DB_game_list()
        if len(game) > 10:
            self.db.delete_game(game[0])

        games = self.db.get_DB_game_list()

        if name not in games or self.db.get_game_review_number(name) < self.config["add_review_number"]:
            if self.db.add_reviews(name, n=self.config["add_review_number"]):
                noID = True
            else:
                noID = False
        
        if self.db.get_game_review_number(name) < 100:
            return False, noID
        return True, noID

    def get_length(self, documents):
        # get total number of tokens in documents

        total_length = 0
        for document in documents:
            for text in document:
                total_length += len(text)

        return total_length

    def set_document(self, name):
        # add reviews to document from db regarding to keywords
        # limit document length to 1000
        # return document as string

        documents = []
        list_docs = []
        str_docs = ''

        for keyword in self.config["keywords"]:
            document = self.db.get_query_text(name, keyword, n=20, max_len=self.config["max_docs_length"]) # get document number = n * keywords number
            documents.append(document)
        
        while self.get_length(documents) > self.config["total_document_length"]:
            for document in documents:
                document.pop(len(document)-1)

        for document in documents:
            for text in document:
                str_docs += text + ' '
                list_docs.append(text)

        return str_docs, list_docs

    def set_prompt(self):
        # Define the prompt template for the model        
        template = """ [INST] <<SYS>> Ensure that your response is informative and based on the reviews. <</SYS>>
            Reviews: {game_reviews}
            Prompt: Briefly tell me about the game {name} separating with different categories. [/INST]
            Response: Insert a line break between each category.
            """
        
        prompt = PromptTemplate(template=template, input_variables=['game_reviews', 'name'])
        return template, prompt
    
    def output_chain(self, name, id, enoughreview, document, template, prompt):
        # Define the chain of models to be used
        if id == False:
            return "game not found on Steam. Please check the game name."
        elif document == '':
            return "No reviews found for the game."
        elif not enoughreview:
            return "Not enough reviews found for the game."
        
        question = template.format(game_reviews=document, name=name)
        result = self.llm(question, prompt, document, name)
        return result

    def test_chain():
        # test chain, not for practical use
        games = ['Forza Horizon 4', 'Cyberpunk 2077', 'The Witcher 3: Wild Hunt', 'Grand Theft Auto V', 
                 'Red Dead Redemption 2', 'The Legend of Zelda: Breath of the Wild', 'The Elder Scrolls V: Skyrim', 
                 'The Last of Us Part II', 'God of War', 'Horizon Zero Dawn']
        
        testChain = Chain()
        for game in games:
            response = testChain(game)
            print("{game}: ", game, response)

    def eval_chain(self, name):
        enoughreview, id =  self.update_db(name) # update db and add reviews
        template, prompt = self.set_prompt()
        str_docs, list_docs = self.set_document(name)
        result = self.output_chain(name, id, enoughreview, str_docs, template, prompt)
        return list_docs, result

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
# template = """
#         <s>[INST]<<SYS>>
#         You are an AI assistant.
#         Ensure that your response is informative and based on the provided reviews.
#         <</SYS>>
#         Reviews:{game_reviews}
#         Prompt: Summarize the reviews for {name}.
#         [/INST]
#         """
# prompt = PromptTemplate(template=template, input_variables=['game_reviews', 'name'])
# #llm_chain = LLMChain(prompt=prompt, llm=llm.model) # if dictionary time needed
# llm_chain = prompt | llm.model # if only string type output result needed
# gamereviews = "['A fun game to play and I love how the cars are', 'I am hooked to this thing. It is fun. Can you believe that? A fun game?', 'its a fun multi and single player game with lots to do', 'Bought this game thinking that my friends who also bought it would play with me. Boy was I wrong. Fun game though will continue to be sad and play alone.', 'Wonderful game. If you are so done with your life this game can help you']"
# result = llm_chain.invoke({"game_reviews": gamereviews, "name": "Forza Horizon 4"})
# print("result: ")
# print(result)