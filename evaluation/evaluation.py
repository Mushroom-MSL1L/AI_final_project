from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
import re
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean, cityblock, jaccard, canberra, braycurtis
from scipy.stats import binomtest

nltk.download('stopwords')

class TFIDF() :
    def __init__(self):
        self.tiv = TfidfVectorizer(use_idf=True, smooth_idf=True, norm=None, stop_words=stopwords.words('english'))
        self.data = [] # list of strings
        self.tiv_fit = None
        self.tfidf_dict = {}
        self.average_tfidf = []

    def load_data(self, data):
        self.data = data
        self.tiv_fit = self.tiv.fit_transform(data)
        self.make_tfidf_dict()
        self.make_average_tfidf()
    
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

    def make_average_tfidf(self):
        all_scores = self.tiv_fit.toarray()
        sum_scores = np.sum(all_scores, axis=0)
        norm = np.linalg.norm(sum_scores)
        self.average_tfidf = sum_scores / norm

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

    def only_idf_evaluate(self, row_data, n=100):
        if len(row_data) == 0 or n == 0:
            return 0
        lowest_features, _ = self.get_lowest_tfidf_scores(n)
        object_data = self.extract_unique_words(row_data)
        is_exist = []
        for feature in lowest_features:
            is_exist.append(1 if feature in object_data else 0)
        return sum(is_exist) / n

    def take_nomarlize(self, row_data):
        normed_row_data = self.tiv.transform([row_data]).toarray()[0] / np.linalg.norm(self.tiv.transform([row_data]).toarray()[0])
        return normed_row_data

    def get_path (self, file_name):
        current_file_path = os.path.realpath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        file_path = os.path.join(current_dir_path, file_name)
        return file_path
    
    def all_evaluate(self, row_data):
        data_score = self.tiv.transform([row_data]).toarray()[0]
        if np.all(np.array(data_score) == 0):
            print("There is no data to compare.")
            return [0, 0, 0, 0, 0, 0]
        normed_row_data = self.take_nomarlize(row_data)
        scores = self.average_tfidf
        
        cosim = cosine_similarity([scores], [normed_row_data])
        eucl = euclidean(scores, normed_row_data)
        city = cityblock(scores, normed_row_data)
        jac = jaccard(scores, normed_row_data)
        canb = canberra(scores, normed_row_data)
        bray = braycurtis(scores, normed_row_data)
        return [cosim[0][0], eucl, city, jac, canb, bray]
    
    def cosine_similarity(self, row_data):
        normed_row_data = self.take_nomarlize(row_data)
        scores = self.average_tfidf
        cosim = cosine_similarity([scores], [normed_row_data])
        return cosim[0][0]
    
    def conpare_with_cosine_similarity(self, row_data, challenger_data):
        data_cos = self.cosine_similarity(row_data)
        challenger_cos = self.cosine_similarity(challenger_data)
        if data_cos > challenger_cos:
            print("Our model is better.")
        elif data_cos < challenger_cos:
            print("Challenger model is better.")

    
    def signed_rank_test (self, model_evaluations, challenger_evaluations, alpha=0.2):
        n = len(model_evaluations)
        if n != len(challenger_evaluations) or n == 0:
            return None
        if np.all(model_evaluations == challenger_evaluations):
            print("The difference is not statistically significant.")
            return None

        if np.all(np.array(model_evaluations) == 0) or np.all(np.array(challenger_evaluations) == 0):
            print("There is no data to compare.")
            return None
        signed_ranks = []
        for i in range(n):
            signed_ranks.append(model_evaluations[i] - challenger_evaluations[i])
        signed_ranks = np.array(signed_ranks)
        positive_ranks = 0
        if (signed_ranks[0] > 0) : 
            positive_ranks += 1
        for i in range(1, n):
            if signed_ranks[i] < 0:
                positive_ranks += 1
        zero_ranks = np.sum(signed_ranks == 0)
        if zero_ranks == n:
            print("The difference is not statistically significant.")
            return 
        reslt = binomtest(k = positive_ranks, n = n - zero_ranks, p = 0.5, alternative='two-sided')
        p_value = reslt.pvalue
        if p_value < alpha:
            print("The difference is statistically significant.")
            if positive_ranks >= (n - zero_ranks) / 2:
                print("Our model is better.")
            else:
                print("Challenger model is better.")
        else:
            print("The difference is not statistically significant.")


example_data = [
    "This is a test example.",
    "Another test example with different words.",
    "More text data to test TFIDF vectorizer.",
    "More text data to test TFIDF vectorizer.",
    "More text data to test TFIDF vectorizer.",
    "More text data to test TFIDF vectorizer.",
    "More text data to test TFIDF vectorizer.",
]
## example 1
## only_idf_evaluate with example data
# tfidf = TFIDF()
# tfidf.load_data(example_data)
# print("Features:", tfidf.get_features())
# print("feature scores:\n", tfidf.tfidf_dict)
# lowest_tfidf_scores = tfidf.get_lowest_tfidf_scores(n=3)
# print("lowest TF-IDF Scores:", lowest_tfidf_scores[1])
# print("lowest Features:", lowest_tfidf_scores[0])
# print("only_idf_evaluate:", tfidf.only_idf_evaluate(" is a test TFIDF. ", n=3))

## example 2
## only_idf_evaluate with Forza Horizon 4 reviews
# tfidf = TFIDF()
# data_path = tfidf.get_path("../DB/data/Forza Horizon 4_reviews.txt")
# tfidf.load_data_from_file(data_path)
# lowest_tfidf_scores = tfidf.get_lowest_tfidf_scores(n=100)
# print("lowest TF-IDF Scores:", lowest_tfidf_scores[1])
# print("lowest Features:", lowest_tfidf_scores[0])
# print("only_idf_evaluate:", tfidf.only_idf_evaluate(" is a test Forza. ", n=100))

## example 3
## evaluate_average with example data
# tfidf = TFIDF()
# tfidf.load_data(example_data)
# print("Features:", tfidf.get_features())
# print("feature scores:\n", tfidf.tfidf_dict)
# print("average TF-IDF Scores:", tfidf.average_tfidf)
# tfidf.evaluate_average(" is a test TFIDF. ")
# print("evaluate_average:", tfidf.evaluate_average(" is a test TFIDF. "))

## example 4
## evaluate with all distance metrics
# tfidf = TFIDF()
# tfidf.load_data(example_data)
# print("Features:", tfidf.get_features())
# print("feature scores:\n", tfidf.tfidf_dict)
# print("average TF-IDF Scores:", tfidf.average_tfidf)
# data_evaluations = tfidf.all_evaluate("This is a test TFIDF data. ")
# challenger_evaluations = tfidf.all_evaluate("what is this data. ")
# print("all_evaluation:", data_evaluations)
# print("all_evaluation:", challenger_evaluations)
# tfidf.signed_rank_test(data_evaluations, challenger_evaluations, alpha=0.4)

## example 5
## compare with cosine similarity
# tfidf = TFIDF()
# tfidf.load_data(example_data)
# print("Features:", tfidf.get_features())
# print("feature scores:\n", tfidf.tfidf_dict)
# print("average TF-IDF Scores:", tfidf.average_tfidf)
# data_cos = tfidf.cosine_similarity("This is a test TFIDF data. ")
# challenger_cos = tfidf.cosine_similarity("what is this data. ")
# print("data_cos:", data_cos)
# print("challenger_cos:", challenger_cos)
# tfidf.conpare_with_cosine_similarity("This is a test TFIDF data. ", "what is this data. ")