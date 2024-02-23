from PlayerList import hitRate, hitRateList, pastPlayer, pastPlayerList
from scrapeGamelog import scrapeGamelog
from scrapeGamelog import calcHitRate
from updateList import openSpreadsheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#reads, finds, and prints data
def prevCheck(worksheet):
    List = pastPlayerList() #begin instance of class
    spreadsheet = openSpreadsheet() #open the spreadsheeet

    #open sheet to read from
    hitSheet = spreadsheet.worksheet('NHLHitRate')
    nhlList.loadBase(hitSheet)
    
    #add gamelog to check prvious game
    nhlList = scrapeGamelog(nhlList)


# Records parameters from the previous day, saves them to another sheet with hit or miss, and records correlation
if __name__ == "__main__":

    
    