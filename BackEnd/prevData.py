#to be run after the games each day and add data to the correlation sheet

from PlayerList import hitRate, hitRateList, pastPlayer, pastPlayerList
from scrapeGamelog import scrapeGamelog
from scrapeGamelog import calcHitRate
from updateList import openSpreadsheet
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


#reads, finds, and prints data
#returns correlation and p value for hitRate
def prevCheckHitRate():
    nbaList = pastPlayerList() #create list
    spreadsheet = openSpreadsheet() #open the spreadsheeet

    nbaSheet = spreadsheet.worksheet('NBAHitRate')
    nbaList.load_data(nbaSheet, 'nba') #add all info to nbaList

    #add gamelog to check prvious game
    nbaList = scrapeGamelog(nbaList)

    nbaList.check_for_hit()


    prevList = spreadsheet.worksheet('prevNBAHitRate')
    nbaList.load_prev_data(prevList, 'nba') #read from previous list and add it to the back of the existing list

    nbaList.find_corr() #calculate spearman's coefficient

    nbaList.print_to_excel(prevList)

    return nbaList.correlation, nbaList.p_value

def prevAvg():
    nbaList = pastPlayerList() #create list
    spreadsheet = openSpreadsheet() #open the spreadsheeet

    nbaSheet = spreadsheet.worksheet('NBAAvg')
    nbaList.load_data(nbaSheet, 'nba') #add all info to nbaList

    #add gamelog to check prvious game
    nbaList = scrapeGamelog(nbaList)

    nbaList.check_for_hit()


    prevList = spreadsheet.worksheet('prevNBAAvg')
    nbaList.load_prev_data(prevList, 'nba') #read from previous list and add it to the back of the existing list

    nbaList.find_corr() #calculate spearman's coefficient

    nbaList.print_to_excel(prevList)

    return nbaList.correlation, nbaList.p_value


#print the day's correlation to the given log
def printCorr(corr, p):
    spreadsheet = openSpreadsheet()


# Records parameters from the previous day, saves them to another sheet with hit or miss, and records correlation
if __name__ == "__main__":

    #manage additions to the correlation list based on day of the week
    hitRate_corr, hitRate_p_val = prevCheckHitRate()
    #prevAvg()


