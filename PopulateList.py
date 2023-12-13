from PlayerList import PlayerList, Player
import requests
import urllib
from datetime import datetime
import time
import math

BASE_URL = 'https://api.prop-odds.com'
API_KEY = 'NLBqtsuNK9uS9gpboWnB1z6c84Vwk0HIqpLcfmw4'

def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}

def get_usage():
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/usage' + '?' + params
    return get_request(url)

def get_fantasy_snapshot(league, market):
    query_params = {
        'api_key': API_KEY,
        'active_only': False
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/v1/fantasy_snapshot/' + league + '/' + market + '?' + params
    return get_request(url)


    
#import playerList with all the bets from the given sport and stat inputted
def populateBets(playerList, sport, stat):
    
    response = get_fantasy_snapshot(sport, stat)

    statMap = {
        'player_points_over_under' : ['Pts'],
        'player_assists_over_under' : ['Ast'],
        'player_assists_points_over_under' : ['Pts', 'Ast'],
        'player_rebounds_over_under' : ['Reb'],
        'player_points_rebounds_over_under' : ['Pts', 'Reb'],
    }

    # Loop through each bookmaker
    for book in response['fantasy_books']:
        # Check if the bookmaker is PrizePicks
        if book['bookie_key'] == 'prizepicks':
            # Loop through each line in the market and extract participant names
            for line in book['market']['lines']:
                name = line['participant_name']
                projection = line['line']
                player = Player(name, statMap[stat], float(projection), sport)
                playerList.add_player(player)

    return playerList
