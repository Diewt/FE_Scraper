import requests
from bs4 import BeautifulSoup

# Base URL for the main site I will be scraping from
base_url = 'https://serenesforest.net/'


# Consider Converting into a Dictionary
game_url = [
    'shadow-dragon-and-blade-of-light/',
    'gaiden/',
    'mystery-of-the-emblem/',
    'genealogy-of-the-holy-war/',
    'thracia-776/',
    'bs-fire-emblem/',
    'binding-blade/',
    'blazing-sword/',
    'the-sacred-stones/',
    'path-of-radiance/',
    'radiant-dawn/',
    'shadow-dragon/',
    'light-and-shadow/',
    'awakening/',
    'fire-emblem-fates/',
    'fire-emblem-echoes-shadows-valentia/',
    'fire-emblem-heroes/',
    'three-houses/'
]

# Dictionary Containing the additional url info for specific pages based on game
info_url = {
    'shadowDragonDSBaseStats': 'characters/base-stats/default/',
    'shadowDragonDSstatGrowth': 'characters/growth-rates/all/'
}

# Function to parse through the relevant information for Shadow Dragon
# I don't know if the other pages are set up similarly so Shadow dragon will have its own function for parsing
# until further research.
def shadowDragonDS():
    # Constructing the url for the base Stat
    page = base_url + game_url[11] + info_url['shadowDragonDSBaseStats']

    # Setting up the request to get page information and printing out success if possible
    try:     
        r = requests.get(page)
        print('Shadow Dragon DS:')
        print(r.status_code)
    except:
        print('Something went wrong with requesting information about the url')
        return

    # Setting up the web scrapper using Beautiful Soup
    soup = BeautifulSoup(r.content, 'html.parser')
    html = list(soup.children)[3]
    info = soup.find(class_='entry').get_text()
    print(info)
