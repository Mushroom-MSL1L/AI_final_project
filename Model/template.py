from langchain_core.prompts import PromptTemplate

class Template:
    def __init__(self):
        self.template = self.set_template()
        self.cpu_template = self.cpu_template()
        self.score_template = self.set_score_template()
        self.only_score_template = self.set_onlyscore_template()

    def get_template(self):
        return self.template

    def get_cpu_template(self):
        return self.cpu_template
    
    def get_score_template(self):
        return self.score_template

    def get_only_score_template(self):
        return self.only_score_template

    def cpu_template(self):
        template = """ [INST] <<SYS>> Ensure that your response is informative 
                and based on the reviews. <</SYS>>
                Reviews: {game_reviews}
                Prompt: Briefly tell me about the game, {name}, with different categories.
                Response: Break line for each categories [/INST]
                """
        return template

    def set_template(self):
        template = """ [INST] <<SYS>> Ensure that your response is informative and based on the reviews. <</SYS>>
                Reviews: {game_reviews}
                Prompt: Briefly tell me about the game {name} separating with different categories. example: graphic, gameplay.
                Response: break line for each categories [/INST]
                """
        return template

    def set_score_template(self):
        score_template = """
                [INST] 

                Game Name: {name}

                Game Reviews: {game_reviews}

                Model Output: {model_output}

                Evaluation Criteria:

                (1) Your goal is to evaluate the relevance of the content in the Model Output to the categories in the Game Reviews.

                (2) If the Model Output contains ANY keywords or semantic meaning related to the categories in the Game Reviews, consider them relevant.

                (3) It is OK if the Model Output has SOME information that is unrelated to the categories as long as (2) is met.

                Score:

                A score from 0 to 10 will be given based on the following criteria:

                10: The Model Output is entirely relevant to the Game Reviews with no unrelated content.
                7-9: The Model Output is mostly relevant to the Game Reviews with minimal unrelated content.
                4-6: The Model Output is somewhat relevant to the Game Reviews but contains significant unrelated content.
                1-3: The Model Output has little relevance to the Game Reviews and contains mostly unrelated content.
                0: The Model Output is completely unrelated to the Game Reviews.
                Explain your reasoning in a step-by-step manner to ensure your reasoning and conclusion are correct.

                Avoid simply stating the correct answer at the outset.

                Example Evaluation:
                Model Output:
                "The game has stunning visuals with a unique art style that stands out."

                Game Reviews:
                "The visuals are a key highlight, with a unique art style and high graphical fidelity."

                Step-by-Step Evaluation:

                Identify keywords in the Model Output: "stunning visuals," "unique art style."
                Compare with the Game Reviews: The keywords match those in the Game Reviews.
                Check for relevance: The keywords directly relate to the visual aspects of the game as mentioned in the Game Reviews.
                Conclusion: The Model Output is highly relevant to the Game Reviews with no unrelated content.
                Score: 10

                Model Output:
                "The game is very challenging, and the controls are intuitive."

                Game Reviews:
                "The gameplay is challenging, with intuitive controls that enhance the experience."

                Step-by-Step Evaluation:

                Identify keywords in the Model Output: "challenging," "controls," "intuitive."
                Compare with the Game Reviews: The keywords match those in the Game Reviews.
                Check for relevance: The keywords directly relate to gameplay mechanics and controls as mentioned in the Game Reviews.
                Conclusion: The Model Output is highly relevant to the Game Reviews with minimal unrelated content.
                Score: 9

                Model Output:
                "The game has a great story but the multiplayer mode is lackluster."

                Game Reviews:
                "The narrative is engaging, but the multiplayer mode feels underdeveloped."

                Step-by-Step Evaluation:

                Identify keywords in the Model Output: "great story," "multiplayer mode," "lackluster."
                Compare with the Game Reviews: The keywords match those in the Game Reviews.
                Check for relevance: The keywords directly relate to the narrative and multiplayer mode as mentioned in the Game Reviews.
                Conclusion: The Model Output is relevant to the Game Reviews but mentions multiplayer, which might be considered slightly off-topic if the focus is on the story alone.
                Score: 8

                Explanation:
                For each section of the Model Output, identify keywords and their relevance to the Game Reviews. Explain your reasoning step-by-step before assigning a score. This method ensures a thorough and accurate evaluation.
                [/INST]
                """
        return score_template

    def set_onlyscore_template(self):
        only_score_template = """ [INST] 

                Game Name: {name}

                Game Reviews: {game_reviews}

                Model Output: {model_output}

                Evaluation Criteria:

                (1) Your goal is to evaluate the relevance of the content in the Model Output to the categories in the Game Reviews.

                (2) If the Model Output contains ANY keywords or semantic meaning related to the categories in the Game Reviews, consider them relevant.

                (3) It is OK if the Model Output has SOME information that is unrelated to the categories as long as (2) is met.

                Score:

                A score from 0 to 10 will be given based on the following criteria:

                10: The Model Output is entirely relevant to the Game Reviews with no unrelated content.
                7-9: The Model Output is mostly relevant to the Game Reviews with minimal unrelated content.
                4-6: The Model Output is somewhat relevant to the Game Reviews but contains significant unrelated content.
                1-3: The Model Output has little relevance to the Game Reviews and contains mostly unrelated content.
                0: The Model Output is completely unrelated to the Game Reviews.

                Scoring Instructions:
                
                Model Output:
                "The game has stunning visuals with a unique art style that stands out."

                Game Reviews:
                "The visuals are a key highlight, with a unique art style and high graphical fidelity."

                Step-by-Step Evaluation:

                Identify keywords in the Model Output: "stunning visuals," "unique art style."
                Compare with the Game Reviews: The keywords match those in the Game Reviews.
                Check for relevance: The keywords directly relate to the visual aspects of the game as mentioned in the Game Reviews.
                Conclusion: The Model Output is highly relevant to the Game Reviews with no unrelated content.
                Score: 10

                Model Output:
                "The game is very challenging, and the controls are intuitive."

                Game Reviews:
                "The gameplay is challenging, with intuitive controls that enhance the experience."

                Step-by-Step Evaluation:

                Identify keywords in the Model Output: "challenging," "controls," "intuitive."
                Compare with the Game Reviews: The keywords match those in the Game Reviews.
                Check for relevance: The keywords directly relate to gameplay mechanics and controls as mentioned in the Game Reviews.
                Conclusion: The Model Output is highly relevant to the Game Reviews with minimal unrelated content.
                Score: 9

                Model Output:
                "The game has a great story but the multiplayer mode is lackluster."

                Game Reviews:
                "The narrative is engaging, but the multiplayer mode feels underdeveloped."

                Step-by-Step Evaluation:

                Identify keywords in the Model Output: "great story," "multiplayer mode," "lackluster."
                Compare with the Game Reviews: The keywords match those in the Game Reviews.
                Check for relevance: The keywords directly relate to the narrative and multiplayer mode as mentioned in the Game Reviews.
                Conclusion: The Model Output is relevant to the Game Reviews but mentions multiplayer, which might be considered slightly off-topic if the focus is on the story alone.
                Score: 8

                No need to provide a step-by-step evaluation.

                Only print the overall score number.
                [/INST]
                """
        return only_score_template