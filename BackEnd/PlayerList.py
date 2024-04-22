import pandas as pd
import openpyxl
from scipy.stats import spearmanr

#for printing to the base sheet
class Player:
    def __init__(self, name, stat, projection, sport):
        self.name = name
        self.stat = stat
        self.projection = projection
        self.sport = sport

#hit rate information
class hitRate(Player):
    def __init__(self, name, stat, projection, sport, dataframe=None):
        super().__init__(name, stat, projection, sport)

        self.statTable = dataframe if dataframe is not None else pd.DataFrame()

        # Hit calculations
        self.hitRate = 0
        self.hits = 0
        self.attempts = 0
        # Correlation data
        self.rank = 0

class avg(Player):
    def __init__(self, name, stat, projection, sport, dataframe=None):
        super().__init__(name, stat, projection, sport)

        self.statTable = dataframe if dataframe is not None else pd.DataFrame()

        self.average = 0
        self.avg_proj_ratio = 0

        self.rank = 0


#used to check if the last ranking was successful
class pastPlayer(Player):
    def __init__(self, name, stat, projection, sport, rank, hit = 0, dataframe=None):
        super().__init__(name, stat, projection, sport)

        self.statTable = dataframe if dataframe is not None else pd.DataFrame()

        #correlation data
        self.rank = rank
        self.hit = hit


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


class hitRateList(PlayerList):

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

    def rank(self): #add a ranking to calculate correlation
        counter = 1
        for player in self.players:
            player.rank = counter
            counter += 1
 
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
        rank = []

        # Extract data from Player objects
        for hitRate in self.players:
            names.append(hitRate.name)
            stats.append(', '.join(str(stat) for stat in hitRate.stat))
            projections.append(hitRate.projection)
            hit_rates.append(f"{hitRate.hitRate:.2%}")
            hits.append(hitRate.hits)
            attempts.append(hitRate.attempts)
            rank.append(hitRate.rank)

        # Prepare the transposed data
        data_transposed = [names, stats, projections, hit_rates, hits, attempts, rank]

        # Transpose the data to organize it by columns
        data_transposed = list(map(list, zip(*data_transposed)))

        header_list = ["Name", "Stat", "Projection", "Hit Rate", "Hits", "Attempts", "Rank"]
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

class avgPlayerList(PlayerList):

    def rank(self): #add a ranking to calculate correlation
        counter = 1
        for player in self.players:
            player.rank = counter
            counter += 1

    def sort_ratio(self):
        self.players.sort(key=lambda player: player.avg_proj_ratio, reverse = True)

    def print_to_excel(self, worksheet):
        # Clear the existing content in the worksheet
        worksheet.clear()

        # Initialize lists for each attribute
        names = []
        stats = []
        projections = []
        average = []
        avg_proj_ratio = []
        rank = []

        # Extract data from Player objects
        for avg in self.players:
            names.append(avg.name)
            stats.append(', '.join(str(stat) for stat in avg.stat))
            projections.append(avg.projection)
            average.append(avg.average)
            avg_proj_ratio.append(avg.avg_proj_ratio)
            rank.append(avg.rank)

        # Prepare the transposed data
        data_transposed = [names, stats, projections, average, avg_proj_ratio, rank]

        # Transpose the data to organize it by columns
        data_transposed = list(map(list, zip(*data_transposed)))

        header_list = ["Name", "Stat", "Projection", "Average", "Avg/Proj", "Rank"]
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

            player = avg(name, stat, projection, sport)

            # Add the player to the player list
            self.add_player(player)


#reads, checks, and prints from excel
class pastPlayerList(PlayerList):

    def __init__(self):
        self.players = []
        self.correlation = 0
        self.p_value = 0

    def print_to_excel(self, worksheet): #print to see a general overview of correlation
        # Clear the existing content in the worksheet
        worksheet.clear()

        # Initialize lists for each attribute
        names = []
        stats = []
        projections = []

        rank = []
        hit = []

        # Extract data from Player objects
        for player in self.players:
            names.append(player.name)
            stats.append(', '.join(str(stat) for stat in player.stat))
            projections.append(player.projection)

            rank.append(player.rank)
            hit.append(player.hit)

        # Prepare the transposed data
        data_transposed = [names, stats, projections, rank, hit]

        # Transpose the data to organize it by columns
        data_transposed = list(map(list, zip(*data_transposed)))

        header_list = ["Name", "Stat", "Projection", "Rank", "Hit"]
        worksheet.update('A1', [header_list])

        # Update the worksheet with the transposed data starting from cell A1
        worksheet.update('A2', data_transposed)

        #print correlation
        worksheet.update('F1', 'Correlation:')
        worksheet.update('F2', 'P Value')
        worksheet.update('G1', self.correlation)
        worksheet.update('G2', self.p_value)


    def load_data(self, worksheet, sport):
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
            rank = row['Rank']

            player = pastPlayer(name, stat, projection, sport, rank)

            # Add the player to the player list
            self.add_player(player)
    
    def load_prev_data(self, worksheet, sport):
        # Extract all records from the worksheet
        records = worksheet.get_all_records()

        # Convert records to a pandas DataFrame
        df = pd.DataFrame(records)

        # Iterate over the rows in the DataFrame
        for index, row in df.iterrows():
            # Create a new Player object with the data from the row
            name = row['Name']
            stat = row['Stat'].split(', ')
            projection = row['Projection']
            rank = row['Rank']
            hit = row['Hit']

            player = pastPlayer(name, stat, projection, sport, rank, hit)

            # Add the player to the player list
            self.add_player(player)

    def check_for_hit(self):
        # 0 for tie, -1 for miss, 1 for hit

        for player in self.players: #iterate through each player

            #map in which keys represent name of stat, and values represent headers of each gamelog dataframe column
            statMap = {
                #basketball
                "Pts" : "PTS",
                "Ast" : "AST",
                "Reb" : "REB",
                "Stl" : "STL",
                "Blk" : "BLK",
                "3PM" : "3PM",
                "TO" : "TO",
            
            }

            #replace stat names from player_props with stat names from fantasy pros
            mapped_stats = []
            if isinstance(player.stat, str):  # Check if player.stat is a string
                if player.stat in statMap:
                    mapped_stats.append(statMap[player.stat])
                else:
                    mapped_stats.append(player.stat)
            else:  # Assuming player.stat is a list of strings
                for stat in player.stat:
                    if stat in statMap:
                        mapped_stats.append(statMap[stat])
                    else:
                        mapped_stats.append(stat)

            if mapped_stats[0] in player.statTable.columns:

                for stat in mapped_stats:

                    # Filter out rows with non-numeric values in stat column
                    filtered_statTable = player.statTable[pd.notnull(player.statTable[stat])]
                    # Convert 'stat' column to numeric, coercing non-convertible values to NaN
                    filtered_statTable[stat] = pd.to_numeric(filtered_statTable[stat], errors='coerce')

                game_sum = 0
                check_numeric = 1
                for stat in mapped_stats:

                    # Check if there is a string value in the table, and if so, it is going to print -20 in the excel for me to know
                    if isinstance(filtered_statTable[stat].iloc[0], (str)):
                        check_numeric = 0
                    else:
                        game_sum += filtered_statTable[stat].iloc[0]
            
            if check_numeric == 0: #error with the gamesum
                player.hit = -20
            elif game_sum > player.projection:
                player.hit = 1
            elif game_sum == player.projection:
                player.hit = 0
            else:
                player.hit = -1

    def find_corr(self):
        
        ranks = [player.rank for player in self.players]
        hits = [player.hit for player in self.players]

        spearman_coefficient, p_value = spearmanr(ranks, hits)

        self.correlation = spearman_coefficient
        self.p_value = p_value
