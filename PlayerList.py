import pandas as pd
import openpyxl

class Player:
    def __init__(self, name, position, stat, projection, sport, dataframe=None):
        self.name = name
        self.position = position
        self.stat = stat
        self.projection = projection
        self.sport = sport
        #data fram imported from recent games
        self.statTable = dataframe if dataframe is not None else pd.DataFrame()

        #hit calcaultions
        self.hitRate = 0
        self.hits = 0
        self.attempts = 0

    def split_stat(self):
        if isinstance(self.stat, list):  # Checking if stat is a list
            return self.stat  # If it's already a list, return it as is

        # Splitting stat on '+' if it contains '+'
        if '+' in self.stat:
            split_list = self.stat.split('+')  # Splitting and returning as a list
            for i, item in enumerate(split_list):
                split_list[i] = item.strip()  # Stripping whitespace and updating the list item
            return split_list
        else:
            return [self.stat]  # If no '+', return a list with the single stat element



class PlayerList:
    def __init__(self):
        self.players = [] #initialize empty list for players

    def clear_list(self):
        # Clear the contents of the player list
        self.players = []
    
    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player_name):
        for player in self.players:
            if player.name == player_name:
                self.players.remove(player)
                return
    
    def get_player_by_name(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player
        return None

    def num_players(self):
        return len(self.players)
    
    def calculate_hit_percentages(self):
        for player in self.players:
            if player.attempts == 0:
                player.hitRate = 0
            else:
                player.hitRate = player.hits / player.attempts

    def split_stat_list(self):
        for player in self.players:
            player.stat = player.split_stat()

    def sort_by_hit_percentage(self):
        self.players.sort(key=lambda player: player.hitRate, reverse = True)

    def print_list(self):
        for player in self.players:
            print(f"{player.name}, {player.stat}: Hit Rate - {player.hitRate:.2%} - {player.hits} / {player.attempts}")
 
    def print_to_excel(self, worksheet):
        # Clear the existing content in the worksheet
        worksheet.clear()

        # Initialize lists for each attribute
        names = []
        positions = []
        stats = []
        projections = []
        sports = []
        hit_rates = []
        hits = []
        attempts = []

        # Extract data from Player objects
        for player in self.players:
            names.append(player.name)
            positions.append(player.position)
            stats.append(', '.join(str(stat) for stat in player.stat))
            projections.append(player.projection)
            sports.append(player.sport)
            hit_rates.append(f"{player.hitRate:.2%}")
            hits.append(player.hits)
            attempts.append(player.attempts)

        # Prepare the transposed data
        data_transposed = [names, positions, stats, projections, sports, hit_rates, hits, attempts]

        # Transpose the data to organize it by columns
        data_transposed = list(map(list, zip(*data_transposed)))

        header_list = ["Name", "Position", "Stat", "Projection", "Sport", "Hit Rate", "Hits", "Attempts"]
        worksheet.update('A1', [header_list])

        # Update the worksheet with the transposed data starting from cell A1
        worksheet.update('A2', data_transposed)