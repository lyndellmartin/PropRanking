from PlayerList import hitRate, hitRateList
import pandas as pd
import requests
import math
import re
from collections.abc import Iterable

#goes from multilevel to single level
def flattenFrame(statTable):

    #statTable.rename(columns=new_column_names, level=1, inplace=True)
    # Flatten the MultiIndex columns
    statTable.columns = ['_'.join(col).strip() if isinstance(col, Iterable) and not isinstance(col, str) else col for col in statTable.columns.values]

    return statTable


#saves a panda table to each of the players
def scrapeGamelog(hitRateList):

    counter = 0

    pattern = re.compile('[^a-zA-Z ]')
    for player in hitRateList.players:

        #prepare URL
        names = player.name.split()
        cleansed_names = []
        cleansed_names2 = []
    

        #Special cases for names
        # Process names containing hyphens
        for part in names:
            if '-' in part:
                hyphen_split = part.split('-')
                cleansed_names.extend(hyphen_split)
            else:
                cleansed_names.append(part)

        # Process names containing other special characters
        for name in cleansed_names:
            cleansed_name2 = pattern.sub('', name)
            cleansed_names2.append(cleansed_name2)

        #handling special cases such as nic-nicolas
        if cleansed_names2[0] == 'Nic':
            cleansed_names2[0] = 'Nicolas'

        first = cleansed_names2[0].lower()
        last = cleansed_names2[1].lower()
        url = f"https://www.fantasypros.com/{player.sport}/games/{first}-{last}"

        suffix = {"jr", "sr", "ii", "iii", "iv"}
        # Check if Roman numeral was found and add to URL
        if len(cleansed_names2) == 3 and cleansed_names2[2].lower() not in suffix: #case of three names that do not include a suffix
            url += f"-{cleansed_names2[2].lower()}"

        #more special cases
        if cleansed_names2[0] == 'Cameron' and cleansed_names2[1] == "Johnson":
            url += "-g"
        if cleansed_names2[0] == 'Bruce' and cleansed_names2[1] == "Brown":
            url += "-jr"
        if cleansed_names2[0] == 'Jaime' and cleansed_names2[1] == "Jaquez":
            url += "-jr"
        if cleansed_names2[0] == 'Alperen' and cleansed_names2[1] == "Sengun":
            url += "-c"
        
        url += ".php"

        #begin importing process
        headers_list = [
        # Add multiple user-agent strings to rotate
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'},
        ]

        headers = headers_list[counter % len(headers_list)]  # Rotate headers
        session = requests.Session()
        response = session.get(url, headers=headers)

        # Use pandas read_html to parse the HTML table
        dfs = pd.read_html(response.content)

        # If there are multiple tables, dfs will be a list of DataFrames
        if len(dfs) > 0:
            df = dfs[0]  # Accessing the first DataFrame
            player.statTable = df
        else:
            print("No tables found in the HTML")
        
        if player.sport == 'nfl': #if it is nfl(multilevel), clean the table to single level
            player.statTable = flattenFrame(player.statTable)

        counter += 1

    return hitRateList




#uses the dataframes saved to each player to calculate
def calcHitRate(hitRateList):

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
        
        #hockey
        'Goals' : 'G',
        'Assists' : 'ASSISTS',
        'Pts' : 'POINTS',
        'SOG' : 'SOG',
        'Goals Against' : 'GOALS AGAINST',
        'Saves' : 'SAVES',

        #football
        'Ast Tackles' : 'Defense_tackle',
        'FG' : 'Kicking_FG',
        'Pass Att' : 'Passing_att',
        'Pass TD' : 'Passing_TD',
        'Pass YD' : 'Passing_yds',
        'Rec YD' : 'Receiving_yds',
        'Rec' : 'Receiving_rec',
        'Rush Att' : 'Rushing_att',
        'Rush YD' : 'Rushing_att',
        'Sacks' : 'Defense_sack',
        'Ast Tackles' : 'Defense_assist',
    }

    for player in hitRateList.players:

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
            
            game_stats = []
            # Iterate through each row (game) in the DataFrame
            for index, row in player.statTable.iterrows():
                # Initialize sum for the current game
                game_sum = 0

                # Iterate through each stat in the stats_to_extract list
                # Iterate through each stat in the stats_to_extract list
                for stat in mapped_stats:
                    # Check if the value is numeric (int or float) before adding
                    if isinstance(row[stat], (int, float)):
                        game_sum += row[stat]
                    else:
                        # Handle non-numeric values (e.g., strings) if present
                        # You might want to convert them to numeric type before adding
                        try:
                            numeric_value = float(row[stat])  # Convert string to float
                            game_sum += numeric_value
                        except ValueError:
                            print(f"Non-numeric value '{row[stat]}' found in column '{stat}'")

                    
                # Append the aggregated sum for the current game to games_stats
                game_stats.append(game_sum)

            projection = player.projection

            # Count how many times stats are over the projection
            for game in game_stats:
                if isinstance(projection, float) and not projection.is_integer():  # Check if projection is a float
                    if game > projection:
                        player.hits += 1
                    player.attempts += 1 # don't have to check for pushes
                else:  # If projection is an integer or a float with no decimal part
                    if game > projection:
                        player.hits += 1
                    if game != projection:  # Check if game is not equal to projection as an integer
                        player.attempts += 1
                    #if projection is = to game, just ignore it completely not adding either
           
        else: #column not found in dataframe
            print(f"{player.name} ignored due to website behavior")
            hitRateList.remove_player(player.name) #if it does not contain desired stat meaning incorrect table pulled in the case of website behavior

    hitRateList.calculate_hit_percentages()

    return hitRateList


#calculates the average and ratio of projection to avg
def calc_avg(avgPlayerList):

    #map in which keys represent name of stat, and values represent headers of each gamelog dataframe column
    statMap = {
        #basketball
        "Pts" : "PTS",
        "Ast" : "AST",
        "Reb" : "REB",
        "Stl" : "STL",
        "Blk" : "BLK",
        "3PM" : "3PM",
        "TO" : "TO"
    }
    
    for player in avgPlayerList.players:

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
            
            total_sum = 0
            game_counter = 0
            # Iterate through each row (game) in the DataFrame
            for index, row in player.statTable.iterrows():
                # Initialize sum for the current game
                game_sum = 0

                # Iterate through each stat in the stats_to_extract list
                # Iterate through each stat in the stats_to_extract list
                for stat in mapped_stats:
                    # Check if the value is numeric (int or float) before adding
                    if isinstance(row[stat], (int, float)):
                        game_sum += row[stat]
                    else:
                        # Handle non-numeric values (e.g., strings) if present
                        # You might want to convert them to numeric type before adding
                        try:
                            numeric_value = float(row[stat])  # Convert string to float
                            game_sum += numeric_value
                        except ValueError:
                            print(f"Non-numeric value '{row[stat]}' found in column '{stat}'")
                total_sum += game_sum
                game_counter += 1

            player.average = total_sum / game_counter

            player.avg_proj_ratio = player.average / player.projection
           
        else: #column not found in dataframe
            print(f"{player.name} ignored due to website behavior")
            avgPlayerList.remove_player(player.name) #if it does not contain desired stat meaning incorrect table pulled in the case of website behavior

    return avgPlayerList