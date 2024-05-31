import re
import langid

class preprocess:
    def __init__(self, data=None):
        self.data = data

    def load_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def pick_enough_words(self, n=10):
        temp_data = []
        for i in self.data :
            if len(i.split()) > n:
                temp_data.append(i)
        self.data = temp_data

    def pick_english(self):
        temp_data = []
        for i in self.data:
            if langid.classify(i)[0] == 'en':
                temp_data.append(i)
        self.data = temp_data

    def clean_text(self):
        temp_data = []
        for i in self.data:
            i = re.sub(r'\s+', ' ', i) 
            i = re.sub(r'[^A-Za-z0-9\s.\\\/?!]', '', i) 
            temp_data.append(i)
        self.data = temp_data

    def remove_overflow(self, max_len=110):
        temp_data = []
        for i in self.data:
            small_str = ''
            arr = i.split()
            for counter, j in enumerate(arr):
                if len(arr) < counter:
                    break
                if len(small_str) <= max_len:
                    small_str += j + ' '
                else:
                    break
            temp_data.append(small_str.strip())
        self.data = temp_data
    
    def is_meaningful(self):
        temp_data = []
        for i in self.data:
            flag = True
            if re.search(r'[A-Za-z]', i):
                flag = True
            if re.search(r'(\.|\?|!|/|\\){4,}', i):
                flag = False
            if flag:
                temp_data.append(i)
        self.data = temp_data
