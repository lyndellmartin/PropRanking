from PlayerList import PlayerList, Player
from PopulateList import populateBets
from scrapeGamelog import scrapeGamelog
from scrapeGamelog import calcHitRate
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def openSpreadsheet():

    #set up before program begins running, setting up connection with spreadsheet and initializing playerList

    credentials_file_path = 'player-prop-ranking-d1c6875c72b4.json'

    # Define the scope and credentials from the downloaded JSON file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file_path, scope)
    client = gspread.authorize(credentials)

    spreadsheet_id = '1na9sjEtjP3Oltvhwha-WtBT-f5xSDhC47kcMblB0Lvo'
    spreadsheet = client.open_by_key(spreadsheet_id)

    return spreadsheet

def updateNBA(): #120 requests

    spreadsheet = openSpreadsheet()
    nbaHitRateSheet = spreadsheet.worksheet('NBAHitRate')

    nbaList = PlayerList()
    nbaList = populateBets(nbaList, "nba", "player_points_over_under")
    nbaList = populateBets(nbaList, "nba", "player_assists_over_under")
    nbaList = populateBets(nbaList, "nba", "player_rebounds_over_under")
    nbaList = populateBets(nbaList, "nba", "player_assists_points_over_under")
    nbaList = populateBets(nbaList, "nba", "player_points_rebounds_over_under")
    nbaList = populateBets(nbaList, "nba", "player_assists_points_rebounds_over_under")
    nbaList = populateBets(nbaList, "nba", "player_assists_rebounds_over_under")
    nbaList = populateBets(nbaList, "nba", "player_blocks_steals_over_under")
    nbaList = populateBets(nbaList, "nba", "player_blocks_over_under")
    nbaList = populateBets(nbaList, "nba", "player_steals_over_under")
    nbaList = populateBets(nbaList, "nba", "player_threes_over_under")
    nbaList = populateBets(nbaList, "nba", "player_turnovers_over_under")

    nbaList = scrapeGamelog(nbaList)
    nbaList = calcHitRate(nbaList)
    nbaList.sort_by_hit_percentage()
    
    nbaList.print_to_excel(nbaHitRateSheet)


def updateNHL(): #50 requests

    spreadsheet = openSpreadsheet()
    nhlHitRateSheet = spreadsheet.worksheet('NHLHitRate')

    nhlList = PlayerList()
    nhlList = populateBets(nhlList, "nhl", "player_points_over_under")
    nhlList = populateBets(nhlList, "nhl", "player_assists_over_under")
    nhlList = populateBets(nhlList, "nhl", "player_shots_over_under")
    nhlList = populateBets(nhlList, "nhl", "goalie_goals_over_under")
    nhlList = populateBets(nhlList, "nhl", "goalie_saves_over_under")

    nhlList = scrapeGamelog(nhlList)
    nhlList = calcHitRate(nhlList)
    nhlList.sort_by_hit_percentage()
    
    nhlList.print_to_excel(nhlHitRateSheet)

#Needs troubleshooting, but not in season
def updateNFL(): #130 requests

    spreadsheet = openSpreadsheet()
    nflHitRateSheet = spreadsheet.worksheet('NFLHitRate')

    nflList = PlayerList()
    #nflList = populateBets(nflList, "nfl", "player_td_over_under")
    nflList = populateBets(nflList, "nfl", "player_assisted_tackles_over_under")
    nflList = populateBets(nflList, "nfl", "player_field_goals_over_under")
    nflList = populateBets(nflList, "nfl", "player_passing_attempts_over_under")
    nflList = populateBets(nflList, "nfl", "player_passing_tds_over_under")
    nflList = populateBets(nflList, "nfl", "player_passing_yds_over_under")
    nflList = populateBets(nflList, "nfl", "player_receptions_over_under")
    nflList = populateBets(nflList, "nfl", "player_receiving_yds_over_under")
    nflList = populateBets(nflList, "nfl", "player_rushing_attempts_over_under")
    nflList = populateBets(nflList, "nfl", "player_rushing_yds_over_under")
    nflList = populateBets(nflList, "nfl", "player_sacks_over_under")
    nflList = populateBets(nflList, "nfl", "player_tackles_and_assists_over_under")
    nflList = populateBets(nflList, "nfl", "player_tackles_over_under")

    nflList = scrapeGamelog(nflList)
    nflList = calcHitRate(nflList)
    nflList.sort_by_hit_percentage()

    nflList.print_to_excel(nflHitRateSheet)


#updates the main
if __name__ == "__main__":
    
    updateNFL()
    updateNHL()