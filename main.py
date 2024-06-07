# from Model import Chain
from Evaluation import TFIDF

if __name__ == "__main__":
    # Chain.test_chain()
    tfidf = TFIDF()
    tfidf.load_data_from_file('DB/data/Forza Horizon 4_reviews.txt')
    score = tfidf.evaluate("Forza Horizon 4 is a great game", n=10)
    print(score)
