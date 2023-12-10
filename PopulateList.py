from PlayerList import PlayerList, Player

from bs4 import BeautifulSoup

from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import math

# Function to click the "Next" button or print a message if not found
def click_next(driver):
    try:
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.button--styleless.pbcs-page-pagination__button')))
        driver.execute_script("arguments[0].scrollIntoView();", button)
        button.click()
        print("Clicked the 'Next' button successfully!")
    except Exception as e:
        print(f"Error clicking the button: {e}")

    
#import playerList with all the bets from the given sport and stat inputted
def populateBets(playerList, sport, stat):
    if sport == "nba":
        url = f"https://www.bettingpros.com/nba/picks/prop-bets/bet/{stat}/"
    elif sport == "nfl":
        statMap = {
            "rushing yards": "rushing-yards",
            "passing yards": "passing-yards"
        }
        url = f"https://www.bettingpros.com/nfl/picks/prop-bets/bet/{statMap[stat]}/"

    # Set options for the Edge WebDriver
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('headless')

    # Initialize the Edge WebDriver
    driver = Edge(executable_path='msedgedriver.exe', options=options)

    driver.get(url)
    time.sleep(10)

    # Capture the current page source
    page_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page_source, 'html.parser')
    
    if sport == "nba" or sport == "nfl":
        player_divs = soup.find_all('div', id='primary-info-container')
        for div in player_divs:

            player_card = div.find('div', class_='card__player-container')
            player_name = player_card.find('a', class_='pbcs__player-link').text.strip()
            player_position = player_card.find_all('span', class_='typography')[1].text.strip()

            prop_container = div.find('div', class_='card__prop-container')
            stats = prop_container.find_all('span', class_='typography')
            player_projection = stats[0].text.strip()
            projection_stat = stats[1].text.strip()

            player = Player(player_name, player_position, projection_stat, float(player_projection), sport)
            playerList.add_player(player)

    playerList.split_stat_list()
    return playerList
