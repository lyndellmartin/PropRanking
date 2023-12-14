from PlayerList import PlayerList, Player
from PopulateList import populateBets
from scrapeGamelog import scrapeGamelog
from scrapeGamelog import calcHitRate
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def updateNBA(): #takes around 120 requests but fully updates everything needed

    #set up before program begins running, setting up connection with spreadsheet and initializing playerList

    credentials_file_path = 'player-prop-ranking-d1c6875c72b4.json'

    # Define the scope and credentials from the downloaded JSON file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file_path, scope)
    client = gspread.authorize(credentials)

    spreadsheet_id = '1XDDtz18NOIjRXUS3mYUNoGqp-2_wZt032NOXVj2LBPk'
    spreadsheet = client.open_by_key(spreadsheet_id)

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



if __name__ == "__main__":
    updateNBA()
