import yaml 
import requests
import os
import json

# https://partner.steamgames.com/doc/store/getreviews
class API:
    def __init__(self):
        self.config = self.get_config()
        self.api_key = self.config['steam_api_key']
        self.id_list = self.get_ID_list()

    def get_config(self):
        config = {}
        current_file_path = os.path.realpath(__file__)
        current_dir_path = os.path.dirname(current_file_path)
        config_file_path = os.path.join(current_dir_path, 'config.yaml')
        with open(config_file_path, 'r') as file :
            config = yaml.safe_load(file)
        return config

    def get_ID_list(self):
        url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        response = requests.get(url)
        row_data = response.json()
        return row_data['applist']['apps']
    
    def get_game_Id (self, game_name):
        for game in self.id_list:
            if game['name'] == game_name:
                return game['appid']
        return None 
        
    def get_reviews_information (self, game_id):
        params = {
            "json": "1", 
            "filter": "recent", # recent, updated, all
            # "language": "en",  
            # "day_range": "30",  
            "cursor": "*",
            "review_type": "all", # all, positive, negative
            "purchase_type": "all", # all, non_steam_purchase, steam
            "num_per_page": "100",  
        }
        r = requests.get('https://store.steampowered.com/appreviews/{appid}?json=1'.format(appid=game_id), params=params)
        row_data = r.json()
        if r.status_code == 200:
            if row_data['success'] == 1:
                return json.dumps(row_data['reviews'], indent=4)
            else:
                print('Error: ', row_data['success'])
                return None
        else:
            print('Error: ', r.status_code)
            return None
    
    def get_reviews(self, game_id):
        params = {
            "json": "1", 
            "filter": "recent", # recent, updated, all
            # "language": "en",  
            # "day_range": "30",  
            "cursor": "*",
            "review_type": "all", # all, positive, negative
            "purchase_type": "all", # all, non_steam_purchase, steam
            "num_per_page": "100",  
        }
        r = requests.get('https://store.steampowered.com/appreviews/{appid}?json=1'.format(appid=game_id), params=params)
        row_data = r.json()
        if r.status_code == 200:
            if row_data['success'] == 1:
                reviews_information = row_data['reviews']
            else:
                print('Error: ', row_data['success'])
                return None
        else:
            print('Error: ', r.status_code)
            return None
        
        if reviews_information is not None:
            reviews = []
            for review in reviews_information:
                reviews.append(review['review'])
            return reviews
    
    
a = API()
name = 'The Two Moons'
game_id = a.get_game_Id(name)

r = a.get_reviews(game_id)
print(r)
print(len(r))
# print(a.get_reviews_information(game_id))
# print(a.id_list)