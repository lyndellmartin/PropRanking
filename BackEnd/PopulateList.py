from PlayerList import PlayerList, Player
import requests
import urllib
from datetime import datetime
import time
import math


#Pulling from PropOdds API
BASE_URL = 'https://api.prop-odds.com'
API_KEY = '6dvBiRWWH6aBNjkeG8W89ir3KeihIeyY'

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
        'active_only': True
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/v1/fantasy_snapshot/' + league + '/' + market + '?' + params
    return get_request(url)

    
#import playerList with all the bets from the given sport and stat inputted
def populateBets(playerList, sport, stat):
    
    response = get_fantasy_snapshot(sport, stat)

    statMap = {
        #basketball
        'player_points_over_under' : ['Pts'],
        'player_assists_over_under' : ['Ast'],
        'player_assists_points_over_under' : ['Pts', 'Ast'],
        'player_rebounds_over_under' : ['Reb'],
        'player_points_rebounds_over_under' : ['Pts', 'Reb'],
        'player_assists_points_rebounds_over_under' : ['Pts', 'Ast', 'Reb'],
        'player_assists_rebounds_over_under' : ['Ast', 'Reb'],
        'player_blocks_steals_over_under' : ['Blk', 'Stl'],
        'player_blocks_over_under' : ['Blk'],
        'player_steals_over_under' : ['Stl'],
        'player_threes_over_under' : ['3PM'],
        'player_turnovers_over_under' : ['TO'],
        #hockey
        'player_goals_over_under' : ['Goals'],
        'player_points_over_under' : ['Pts'],
        'player_shots_over_under' : ['SOG'],
        'goalie_goals_over_under' : ['Goals Against'],
        'goalie_saves_over_under' : ['Saves'],
        #football
        'player_assisted_tackles_over_under' : ['Ast Tackles'],
        'player_field_goals_over_under' : ['FG'],
        'player_passing_attempts_over_under' : ['Pass Att'],
        'player_passing_tds_over_under' : ['Pass TD'],
        'player_passing_yds_over_under' : ['Pass YD'],
        'player_receiving_yds_over_under' : ['Rec YD'],
        'player_receptions_over_under' : ['Rec'],
        'player_rushing_attempts_over_under' : ['Rush Att'],
        'player_rushing_yds_over_under' : ['Rush YD'],
        'player_sacks_over_under' : ['Sacks'],
        'player_tackles_and_assists_over_under' : ['Tackles', 'Ast Tackles'],
        'player_tackles_over_under' : ['Tackles'],
        'player_td_over_under' : ['TD']
    }

    count = 0
    # Check if 'response' has content and 'fantasy_books' is in response
    if 'fantasy_books' in response and response['fantasy_books']:
        # Loop through each bookmaker
        for book in response['fantasy_books']:
            # Check if the bookmaker is PrizePicks
            if book['bookie_key'] == 'prizepicks':
                # Loop through each line in the market and extract participant names
                for line in book['market']['lines']:
                    name = line['participant_name']
                    projection = line['line']
                    player = Player(name, statMap[stat], float(projection), sport)
                    if player.sport == "nhl" and player.stat == ['Ast']: #written differently for nhl and nba
                        player.stat = ['Assists']
                    playerList.add_player(player)
                    count += 1
    print(f'{stat} : {count}')
    return playerList
