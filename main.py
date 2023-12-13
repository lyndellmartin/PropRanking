from PlayerList import PlayerList, Player
from PopulateList import populateBets
from scrapeGamelog import scrapeGamelog
from scrapeGamelog import calcHitRate
import gspread
from oauth2client.service_account import ServiceAccountCredentials



if __name__ == "__main__":

    #set up before program begins running, setting up connection with spreadsheet and initializing playerList

    credentials_file_path = 'player-prop-ranking-d1c6875c72b4.json'

    # Define the scope and credentials from the downloaded JSON file
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file_path, scope)
    client = gspread.authorize(credentials)

    spreadsheet_id = '1na9sjEtjP3Oltvhwha-WtBT-f5xSDhC47kcMblB0Lvo'
    spreadsheet = client.open_by_key(spreadsheet_id)

    nbaHitRateSheet = spreadsheet.worksheet('NBAHitRate')

    nbaList = PlayerList()
    nbaList = populateBets(nbaList, "nba", "player_points_over_under")
    nbaList = populateBets(nbaList, "nba", "player_assists_over_under")
    nbaList = populateBets(nbaList, "nba", "player_rebounds_over_under")

    nbaList = scrapeGamelog(nbaList)
    nbaList = calcHitRate(nbaList)
    nbaList.sort_by_hit_percentage()
    
    nbaList.print_to_excel(nbaHitRateSheet)
    nbaList.clear_list()