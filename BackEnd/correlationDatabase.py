from PlayerList import PlayerList, Player
from PopulateList import populateBets
from scrapeGamelog import scrapeGamelog
from scrapeGamelog import calcHitRate
from updateList import openSpreadsheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#reads excel, calculates correlation, updates excel, and updates database
if __name__ == "__main__":

    #setup necessary spreadsheet and list
    nbaList = PlayerList()
    spreadsheet = openSpreadsheet()
    nbaHitRateSheet = spreadsheet.worksheet('NBAHitRate')

    #read list from spreadsheet
    nbaList.load_from_excel(nbaHitRateSheet)

    #scrape game log
    scrapeGamelog(nbaList)

    #check to see if the previous game was a hit or not
    for player in nbaList.players:
        


    #save this list to a database and update the excel sheet
    
    