from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import re
import numpy as np
import os

nltk.download('stopwords')

class TFIDF() :
    def __init__(self):
        self.tiv = TfidfVectorizer(use_idf=True, smooth_idf=True, norm=None, stop_words=stopwords.words('english'))
        self.data = [] # list of strings
        self.tiv_fit = None
        self.tfidf_dict = {}
    
    def load_data(self, data):
        self.data = data
        self.tiv_fit = self.tiv.fit_transform(data)
        self.make_tfidf_dict()
    
    def load_data_from_file(self, file_path):
        temp_data = []
        with open(file_path, 'r') as file:
            while file.readline() != '':
                split_data = file.readline().split('\t')
                temp_data.append(split_data[1])
        self.load_data(temp_data)

    def make_tfidf_dict(self):
        features = self.get_features()
        temp_string = ""
        for i in range(len(features)):
            temp_string += features[i] + " " 
        scores = self.tiv.transform([temp_string]).toarray()
        for i in range(len(features)):
            self.tfidf_dict[features[i]] = scores[0][i]

    def get_features(self):
        return self.tiv.get_feature_names_out()

    def get_lowest_tfidf_scores(self, n):
        if len(self.data) == 0 or n == 0:
            return [], []
        features = self.get_features()
        scores = []
        for i in features:
            scores.append(self.tfidf_dict[i])
        lowest_scores_index = np.argsort(scores)[:n]
        lowest_features = [features[i] for i in lowest_scores_index]
        lowest_scores = [scores[i] for i in lowest_scores_index]

        return lowest_features, lowest_scores

    def extract_unique_words(self, text):
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        words = [word.lower() for word in words]
        unique_words = list(set(words))
        return unique_words

    def evaluate(self, row_data, n=100):
        if len(row_data) == 0 or n == 0:
            return 0
        size = min(n, len(self.data))
        lowest_features, _ = self.get_lowest_tfidf_scores(n)
        object_data = self.extract_unique_words(row_data)
        is_exist = []
        for feature in lowest_features:
            is_exist.append(1 if feature in object_data else 0)
        return sum(is_exist) / size
    
    def get_path (self, file_name):
        current_file_path = os.path.realpath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        file_path = os.path.join(current_dir_path, file_name)
        return file_path


## example 1
# example_data = [
#     "This is a test example.",
#     "Another test example with different words.",
#     "More text data to test TFIDF vectorizer.",
#     "More text data to test TFIDF vectorizer.",
#     "More text data to test TFIDF vectorizer.",
#     "More text data to test TFIDF vectorizer.",
#     "More text data to test TFIDF vectorizer.",
# ]
# tfidf = TFIDF()
# tfidf.load_data(example_data)
# print("Features:", tfidf.get_features())
# print("feature scores:\n", tfidf.tfidf_dict)
# lowest_tfidf_scores = tfidf.get_lowest_tfidf_scores(n=3)
# print("lowest TF-IDF Scores:", lowest_tfidf_scores[1])
# print("lowest Features:", lowest_tfidf_scores[0])
# print("evaluate:", tfidf.evaluate(" is a test TFIDF. ", n=3))

## example 2
# tfidf = TFIDF()
# data_path = tfidf.get_path("../DB/data/Forza Horizon 4_reviews.txt")
# tfidf.load_data_from_file(data_path)
# lowest_tfidf_scores = tfidf.get_lowest_tfidf_scores(n=100)
# print("lowest TF-IDF Scores:", lowest_tfidf_scores[1])
# print("lowest Features:", lowest_tfidf_scores[0])
# print("evaluate:", tfidf.evaluate(" is a test Forza. ", n=100))