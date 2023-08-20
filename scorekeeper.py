import requests
from datetime import datetime


class Match:
    def __init__(self, data,competition=None):
        self.id = int(data['id'])
        self.competition = competition 
        self.date = datetime.strptime(data['date_time_utc'], '%Y-%m-%d %H:%M:%S')
        self.homeTeam = data['team_A']['name']
        self.awayTeam = data['team_B']['name']
        try:
            self.scoreA = data['fts_A'] 
            self.scoreB = data['fts_B'] 
        except:
            self.scoreA = None 
            self.scoreB = None
        self.status = data['status']
    
    def set_date(self, date,hour):
        self.date = date 
        self.hour = hour
    
    def get_date(self):
        return self.date,self.hour
    
    def set_score(self, scoreA, scoreB):
        self.scoreA = scoreA
        self.scoreB = scoreB
        
    def get_score(self):
        return self.scoreA,self.scoreB
    
    def __str__(self):
        return f"{self.homeTeam} - {self.awayTeam}\n{self.date}\n{self.scoreA} - {self.scoreB}"
        

class League:
    def __init__(self, data):
        self.id = data['data']['competition']['id']
        self.name = data['data']['competition']['name']
        self.country = data['data']['competition']['area']['name']
        self.countryId = data['data']['competition']['area']['id']
        
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name
    
    def get_country(self):
        return self.country
    
    def get_country_id(self):
        return self.countryId
    
    def __str__(self):
        return f"League Information:\n  ID: {self.id}\n  Name: {self.name}\n  Country: {self.country}\n  Country ID: {self.countryId}"


def fetch_leagues(start_id=1, end_id=10, api_key="Votre-Clé-API"):
    url = "https://football-live-score-goal-official.p.rapidapi.com/api/v1/competition"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "football-live-score-goal-official.p.rapidapi.com"
    }
    
    leagues_dict = {}
    
    for competition_id in range(start_id, end_id + 1):
        print(competition_id)
        querystring = {"competition_id": str(competition_id)}
        response = requests.get(url, headers=headers, params=querystring)
        
        if response.json()['data'] is not None:
            league = League(response.json())
            leagues_dict[competition_id] = league
            
    return leagues_dict


import json

def league_to_dict(league):
    return {
        'id': league.id,
        'name': league.name,
        'country': league.country,
        'countryId': league.countryId
    }



def dict_to_league(d):
    data = {
        'data': {
            'competition': {
                'id': d['id'],
                'name': d['name'],
                'area': {
                    'name': d['country'],
                    'id': d['countryId']
                }
            }
        }
    }
    return League(data)




#export to json file
def export_to_json(leagues,name='leagues'):
    with open(name+'.json', 'w') as f:
        json.dump({k: league_to_dict(v) for k, v in leagues.items()}, f)

#import from jsonfile
def import_from_json(name='leagues'):
    with open(name+'.json', 'r') as f:
        loaded_dict = json.load(f)
        loaded_leagues = {k: dict_to_league(v) for k, v in loaded_dict.items()}
    return loaded_leagues


'''for i in range(2051,3001,25):
    print(i)
    leagues = fetch_leagues(start_id=i, end_id=i+25-1,api_key="65715b8629mshdf45532b9159fc2p185a71jsne462132de734")
    export_to_json(leagues,f"leagues{i}_{i+25-1}")'''

# Dictionnaire pour stocker toutes les ligues fusionnées
all_leagues = {}

# Liste des noms de fichier à fusionner
# Vous pouvez générer cette liste de noms de fichier selon la manière dont vous les avez organisés
'''file_names = [f"leagues{i}_{i+24}" for i in range(1, 2401, 25)]

# Parcourir chaque fichier et fusionner son contenu dans all_leagues
for name in file_names:
    leagues = import_from_json(name)
    all_leagues.update(leagues)'''

# Si vous voulez, vous pouvez exporter le dictionnaire all_leagues dans un nouveau fichier JSON
#export_to_json(all_leagues, name='all_leagues')

load_league = import_from_json("all_leagues")
max = 0
for i in load_league:
    if(load_league[i].get_country_id()>max):
        max = load_league[i].get_country_id()
print(max)