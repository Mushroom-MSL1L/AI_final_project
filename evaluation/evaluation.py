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
    
    def load_data(self, data):
        self.data = data
        self.tiv_fit = self.tiv.fit_transform(data)
    
    def load_data_from_file(self, file_path):
        temp_data = []
        with open(file_path, 'r') as file:
            while file.readline() != '':
                split_data = file.readline().split('\t')
                temp_data.append(split_data[1])
        self.load_data(temp_data)
                

    def get_features(self):
        return self.tiv.get_feature_names_out()

    def get_highest_tfidf_scores(self, n):
        tfidf_matrix = self.tiv_fit.toarray()
        avg_tfidf_scores = np.mean(tfidf_matrix, axis=0)
        highest_indices = np.argsort(avg_tfidf_scores)[-n:]
        highest_features = [self.get_features()[i] for i in highest_indices]
        highest_scores = [avg_tfidf_scores[i] for i in highest_indices]
        return highest_features, highest_scores

    def extract_unique_words(self, text):
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        words = [word.lower() for word in words]
        unique_words = list(set(words))
        return unique_words

    def evaluate(self, row_data, n=100):
        if len(row_data) == 0 or n == 0:
            return 0
        size = min(n, len(self.data))
        highest_features, _ = self.get_highest_tfidf_scores(n)
        object_data = self.extract_unique_words(row_data)
        is_exist = []
        for feature in highest_features:
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
# highest_tfidf_scores = tfidf.get_highest_tfidf_scores(n=3)
# print("highest TF-IDF Scores:", highest_tfidf_scores[1])
# print("highest Features:", highest_tfidf_scores[0])
# print("evaluate:", tfidf.evaluate(" is a test TFIDF. ", n=3))

## example 2
# tfidf = TFIDF()
# data_path = tfidf.get_path("../DB/data/Forza Horizon 4_reviews.txt")
# tfidf.load_data_from_file(data_path)
# highest_tfidf_scores = tfidf.get_highest_tfidf_scores(n=200)
# print("highest TF-IDF Scores:", highest_tfidf_scores[1])
# print("highest Features:", highest_tfidf_scores[0])
# print("evaluate:", tfidf.evaluate(" is a test Forza. ", n=200))