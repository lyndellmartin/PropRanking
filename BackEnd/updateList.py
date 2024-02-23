from PlayerList import PlayerList, Player, hitRateList, hitRate
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


def updateBaseNBA(): #120 requests

    spreadsheet = openSpreadsheet()
    nbaHitRateSheet = spreadsheet.worksheet('BaseNBA')

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

    nbaList.print_to_excel(nbaHitRateSheet)


def updateBaseNHL(): #50 requests

    spreadsheet = openSpreadsheet()
    nhlSheet = spreadsheet.worksheet('BaseNHL')

    nhlList = PlayerList()
    nhlList = populateBets(nhlList, "nhl", "player_points_over_under")
    nhlList = populateBets(nhlList, "nhl", "player_assists_over_under")
    nhlList = populateBets(nhlList, "nhl", "player_shots_over_under")
    nhlList = populateBets(nhlList, "nhl", "goalie_goals_over_under")
    nhlList = populateBets(nhlList, "nhl", "goalie_saves_over_under")

    nhlList.print_to_excel(nhlSheet)

#read from base and calculate hit rates
def hitRateNHL():

    nhlList = hitRateList() #begin instance of class
    spreadsheet = openSpreadsheet() #open the spreadsheeet

    #open sheet to read from
    baseSheet = spreadsheet.worksheet('BaseNHL')
    nhlList.loadBase(baseSheet)

    nhlList = scrapeGamelog(nhlList)
    nhlList = calcHitRate(nhlList)
    nhlList.sort_by_hit_percentage()

    nhlList.delete_zeros()
    nhlList.rank()

    #Open and print to sheet
    nhlSheet = spreadsheet.worksheet('NHLHitRate')
    nhlList.print_to_excel(nhlSheet)

#read from base and calculate hit rates
def hitRateNBA():

    nbaList = hitRateList() #begin instance of class
    spreadsheet = openSpreadsheet() #open the spreadsheeet

    #open sheet to read from
    baseSheet = spreadsheet.worksheet('BaseNBA')
    nbaList.loadBase(baseSheet)

    nbaList = scrapeGamelog(nbaList)
    nbaList = calcHitRate(nbaList)
    nbaList.sort_by_hit_percentage()

    nbaList.delete_zeros()
    nbaList.rank()

    #Open and print to sheet
    nbaSheet = spreadsheet.worksheet('NBAHitRate')
    nbaList.print_to_excel(nbaSheet)


#updates the list on excel
if __name__ == "__main__":
    

    hitRateNBA()
    hitRateNHL()