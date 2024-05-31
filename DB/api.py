import yaml 
import requests
import os
import json

from tools import get_path
from preprocess import preprocess

# https://partner.steamgames.com/doc/store/getreviews
class API:
    def __init__(self):
        self.id_list = self.get_ID_list()
        self.p = preprocess()

    def get_ID_list(self):
        url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response = requests.get(url)
        row_data = response.json()
        return row_data['applist']['apps']
    
    def show_ID_list(self):
        for game in self.id_list:
            print(game['name'], game['appid'])

    def import_game_list(self):
        file = open(get_path('data/game_list.txt'), 'w')
        for game in self.id_list:
            file.write(str(game['appid']) + '\t' +game['name'] + '\n')

    def get_game_Id (self, game_name):
        for game in self.id_list:
            if game['name'] == game_name:
                return game['appid']
        return None 
        
    def get_reviews_information (self, game_id):
        params = {
            "json": "1", 
            "filter": "recent", # recent, updated, all
            "language": "english",  
            # "day_range": "30",  
            "cursor": "*",
            "review_type": "all", # all, positive, negative
            "purchase_type": "all", # all, non_steam_purchase, steam
            "num_per_page": "3",  
        }
        r = requests.get('https://store.steampowered.com/appreviews/{appid}?json=1'.format(appid=game_id), params=params)
        row_data = r.json()
        if r.status_code == 200:
            if row_data['success'] == 1:
                return json.dumps(row_data['reviews'], indent=4)
            else:
                print('Error: ', row_data['success'])
                return []
        else:
            print('Error: ', r.status_code)
            return []
    
    def get_reviews(self, game_id, n=100, cursor='*'):
        params = {
            "json": "1", 
            "filter": "recent", # recent, updated, all
            "language": "english",  
            # "day_range": "30",  
            "cursor": cursor,
            "review_type": "all", # all, positive, negative
            "purchase_type": "all", # all, non_steam_purchase, steam
            "num_per_page": "100",  
        }
        params['num_per_page'] = str(min(n, 100))
        reviews = []
        row_data = {}
        while len(reviews) < n :
            r = requests.get('https://store.steampowered.com/appreviews/{appid}?json=1'.format(appid=game_id), params=params)
            row_data = r.json()
            if (len(row_data['reviews']) == 0) :
                return reviews, cursor
            temp_reviews = []
            if r.status_code == 200:
                if row_data['success'] == 1:
                    review_information = row_data['reviews']
                    for r in review_information:
                        temp_reviews.append(r['review'])
                    self.p.load_data(temp_reviews)
                    self.p.pick_enough_words(n=10)
                    self.p.clean_text()
                    self.p.pick_enough_words(n=10)
                    self.p.is_meaningful()
                    self.p.pick_english()
                    temp_reviews = self.p.get_data()
                    reviews += temp_reviews
                else:
                    print('Error: ', row_data['success'])
                    return reviews
            else:
                print('Error: ', r.status_code)
                return reviews
            params['cursor'] = row_data['cursor']
            params['num_per_page'] = str(min(n, 100))
        reviews = reviews[:n]
        return reviews, row_data['cursor']
        
    def import_reviews(self, game_id, n=100, cursor='*'):
        reviews, _ = self.get_reviews(game_id=game_id, n=n)
        print(reviews)
        with open(get_path('data/game_review.txt'), 'w') as file:
            for i, review in enumerate(reviews):
                file.write(str(i) + '\t' + review + '\n')
    
    
# a = API() # setup a new API object
# a.import_game_list() # import game list to game_list.txt for human readable

# name = 'Forza Horizon 4' # game name I want to search
# name = 'ELDEN RING' # this game has a lot of reviews
# game_id = a.get_game_Id(name) # get game id by game name

# r, c = a.get_reviews(game_id, n=100) # get reviews of the game by game id
# print("reviews:\n", r, "\n\ncourser:", c)
# a.import_reviews(game_id, n=1000) # import reviews to game_review.txt for human readable
# print(len(r))
# print(a.get_reviews_information(game_id)) # get reviews information of the game by game id