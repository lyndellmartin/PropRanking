import pandas as pd
import openpyxl

#for printing to the base sheet
class Player:
    def __init__(self, name, stat, projection, sport, dataframe=None):
        self.name = name
        self.stat = stat
        self.projection = projection
        self.sport = sport
        #data fram imported from recent games
        self.statTable = dataframe if dataframe is not None else pd.DataFrame()

#for all instances of players
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
    
    def print_to_excel(self, worksheet):
        # Clear the existing content in the worksheet
        worksheet.clear()

        # Initialize lists for each attribute
        names = []
        stats = []
        projections = []
        sports = []
        hit_rates = []
        hits = []
        attempts = []

        # Extract data from Player objects
        for player in self.players:
            names.append(player.name)
            stats.append(', '.join(str(stat) for stat in player.stat))
            projections.append(player.projection)
            sports.append(player.sport)

        # Prepare the transposed data
        data_transposed = [names, stats, projections, sports]

        # Transpose the data to organize it by columns
        data_transposed = list(map(list, zip(*data_transposed)))

        header_list = ["Name", "Stat", "Projection", "Sport"]
        worksheet.update('A1', [header_list])

        # Update the worksheet with the transposed data starting from cell A1
        worksheet.update('A2', data_transposed)
    

#hit rate information
class hitRate(Player):
    def __init__(self, name, stat, projection, sport, dataframe=None):
        self.name = name
        self.stat = stat
        self.projection = projection
        self.sport = sport
        #data fram imported from recent games
        self.statTable = dataframe if dataframe is not None else pd.DataFrame()

        #hit calcaultions
        self.hitRate = 0
        self.hits = 0
        self.attempts = 0


class hitRateList():

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

    #hitRate functions
    def calculate_hit_percentages(self):
        for player in self.players:
            if player.attempts == 0:
                player.hitRate = 0
            else:
                player.hitRate = player.hits / player.attempts

    def delete_zeros(self):
        for i in range(len(self.players) - 1, -1, -1):
            if self.players[i].attempts == 0:
                del self.players[i]

    def sort_by_hit_percentage(self):
        self.players.sort(key=lambda player: player.hitRate, reverse = True)
 
    def print_to_excel(self, worksheet):
        # Clear the existing content in the worksheet
        worksheet.clear()

        # Initialize lists for each attribute
        names = []
        stats = []
        projections = []
        hit_rates = []
        hits = []
        attempts = []

        # Extract data from Player objects
        for hitRate in self.players:
            names.append(hitRate.name)
            stats.append(', '.join(str(stat) for stat in hitRate.stat))
            projections.append(hitRate.projection)
            hit_rates.append(f"{hitRate.hitRate:.2%}")
            hits.append(hitRate.hits)
            attempts.append(hitRate.attempts)

        # Prepare the transposed data
        data_transposed = [names, stats, projections, hit_rates, hits, attempts]

        # Transpose the data to organize it by columns
        data_transposed = list(map(list, zip(*data_transposed)))

        header_list = ["Name", "Stat", "Projection", "Hit Rate", "Hits", "Attempts"]
        worksheet.update('A1', [header_list])

        # Update the worksheet with the transposed data starting from cell A1
        worksheet.update('A2', data_transposed)

    def loadBase(self, worksheet):
        # Extract all records from the worksheet
        records = worksheet.get_all_records()

        # Convert records to a pandas DataFrame
        df = pd.DataFrame(records)

        # Clear the current list
        self.clear_list()

        # Iterate over the rows in the DataFrame
        for index, row in df.iterrows():
            # Create a new Player object with the data from the row
            name = row['Name']
            stat = row['Stat'].split(', ')
            projection = row['Projection']
            sport = row['Sport']

            player = hitRate(name, stat, projection, sport)

            # Add the player to the player list
            self.add_player(player)