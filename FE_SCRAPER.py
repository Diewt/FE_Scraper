from logging import info
import requests
import re
import json
from bs4 import BeautifulSoup

import helper

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
    'shadowDragonDSstatGrowth': 'characters/growth-rates/all/',
    'awakeningSkills' : 'miscellaneous/skills/',
    'awakeningBaseGrowth' : 'characters/growth-rates/base/',
    'awakeningItems' : [
        'inventory/swords/',
        'inventory/lances/',
        'inventory/axes/',
        'inventory/bows/',
        'inventory/tomes/',
        'inventory/staves/',
        'inventory/stones-miscellaneous/',
        'inventory/items/'
    ]
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


# Create json file containing information about skills in Awakening
def FE13Skills():

    # Constructing the url for the skills in awakening
    page = base_url + game_url[13] + info_url['awakeningSkills']

    # Setting up the request to get page information
    try:
        r = requests.get(page)
    except:
        print('Something went wrong with requesting information about the url')
        return

    # Setting up the web scrapper using Beautiful Soup
    soup = BeautifulSoup(r.content, 'html.parser')
    skillTable = soup.find_all('table')

    # Grabbing the first table containing the obtainable skills
    obtainableSkills = skillTable[0].find_all('tr')

    # List containing the values going into the json
    skillList = []

    # Iterate through the first table values and putting them into the List
    for skill in obtainableSkills:
        try:
            columns = skill.find_all('td')
            try:
                data = {
                    'skill': columns[1].text,
                    'effect': columns[2].text,
                    'activation': columns[3].text,
                    'class': columns[4].text,
                    'level': int(columns[5].text)
                }
            except ValueError:
                data = {
                    'skill': columns[1].text,
                    'effect': columns[2].text,
                    'activation': columns[3].text,
                    'class': columns[4].text,
                    'level': columns[5].text
                }
            data = helper.FE13SkillCleaner(data)
            skillList.append(data)
        except IndexError:
            pass

    # Grabbing the Second table containing the enemy only skills
    enemySkills = skillTable[1].find_all('tr')

    # Iterate through the second table values and putting them into the List
    for skill in enemySkills:
        try:
            columns = skill.find_all('td')
            data = {
                'skill': columns[1].text,
                'effect': columns[2].text,
                'activation': columns[3].text,
                'difficulty': columns[4].text,
            }
            data = helper.FE13SkillCleaner(data)
            skillList.append(data)
        except IndexError:
            pass

    with open('skills.json', 'w') as f:
        f.write(json.dumps(skillList, indent=4))


    return

def FE13BaseGrowthRates():
    # Setting up Page Url
    page = base_url + game_url[13] + info_url['awakeningBaseGrowth']

    # Establing request
    try:
        r = requests.get(page)
    except:
        print('Something went wrong with requesting information about the url')
        return

    # Setting up Beautiful Soup
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.find_all('table')

    # Setting up Json List
    baseGrowth = []

    initialCharacters = tables[3].find_all('tr')
    childrenCharacters = tables[4].find_all('tr')
    dlcCharacter = tables[6].find_all('tr')

    for characters in initialCharacters:
        try:
            columns = characters.find_all('td')
            baseGrowth.append( helper.FE13baseGrowthData(columns))
        except IndexError:
            pass

    for characters in childrenCharacters:
        try:
            columns = characters.find_all('td')
            baseGrowth.append( helper.FE13baseGrowthData(columns))
        except IndexError:
            pass

    for characters in dlcCharacter:
        try:
            columns = characters.find_all('td')
            baseGrowth.append( helper.FE13baseGrowthData(columns))
        except IndexError:
            pass

    with open('baseGrowth.json', 'w') as f:
        f.write(json.dumps(baseGrowth, indent=4))


    return

def FE13Items():
    for x in range(len(info_url['awakeningItems'])):
        page = base_url + game_url[13] + info_url['awakeningItems'][x] 

        try:
            r = requests.get(page)
        except:
            print('Something went wrong with requesting information about the url')
            return          

        soup = BeautifulSoup(r.content, 'html.parser')
        items = soup.find_all('tr') 

        for item in items:
            try:
                columns = item.find_all('td')
                print(columns[1].text)
            except IndexError:
                pass
        








