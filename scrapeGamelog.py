from PlayerList import PlayerList, Player
import pandas as pd
import requests
import math
import re

#saves a panda table to each of the players
def scrapeGamelog(playerList):

    counter = 0

    pattern = re.compile('[^a-zA-Z ]')
    for player in playerList.players:

        #prepare URL
        names = player.name.split()
        cleansed_names = []
        cleansed_names2 = []
        
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

        counter += 1

    return playerList




#uses the dataframes saved to each player to calculate
def calcHitRate(playerList):

    statMap = {
        #basketball mapping
        "Pts" : "PTS",
        "Ast" : "AST",
        "Reb" : "REB",
        "Stl" : "STL",
        "Blk" : "BLK",
        "3pts" : "3PM",
        #football mapping
        "Pass TDs": "TD"
    }

    for player in playerList.players:

        #replace stat names from bettingpros with stat names from pro-football reference
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
        elif mapped_stats[0] == "Ftsy score": #if you're dealing with a fantasy score instead of just a regular stat

            fantasy_check = ['PTS', 'REB', 'AST', 'BLK', 'STL', 'TO']
            for stat in fantasy_check: #filter out any non-numeric values in several columns

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

        else:
            print(f"{player.name} ignored due to website behavior")
            playerList.remove_player(player.name) #if it does not contain desired stat meaning incorrect table pulled in the case of website behavior

    playerList.calculate_hit_percentages()

    return playerList