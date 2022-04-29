from asyncio.windows_events import NULL
from logging import info
import requests
import re
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    ],
    'awakeningFullGrowth' : 'characters/growth-rates/full/'
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
            data = helper.FE13SkillCleaner(data, 1)
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
            data = helper.FE13SkillCleaner(data, 2)
            skillList.append(data)
        except IndexError:
            pass

    with open('skills.json', 'w') as f:
        f.write(json.dumps(skillList, indent=4))


    return

# Create json file containing info about character base growth rates in FE13
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

    # Grabbing the nessecary tables on the site
    initialCharacters = tables[3].find_all('tr')
    childrenCharacters = tables[4].find_all('tr')
    dlcCharacter = tables[6].find_all('tr')

    # Next 3 for loops goes through each row in the table and follow same logic
    for characters in initialCharacters:
        try:
            # Grabing information from each column in the row extracted
            columns = characters.find_all('td')

            # Appending information onto final list that will be convered to json
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

    # Write information from baseGrowth into a json file
    with open('baseGrowth.json', 'w') as f:
        f.write(json.dumps(baseGrowth, indent=4))


    return

# Function to scrape full growth page: Investigate how to interact with dropdown select
def FE13FullGrowthRates():

    # Setting up page
    page = base_url + game_url[13] + info_url['awakeningFullGrowth']

    # Access page
    try:
        r = requests.get(page)
    except:
        print('Something went wrong with requesting information about the url')
        return   

    # Setting up Beautiful Soup 
    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.find_all('table')

    # Table 1 = regular characters
    # Table 2 = children characters
    regulars = tables[1].find_all('tr')
    childrens = tables[2].find_all('tr')

    # TODO Plan for extracting with selenium in hand for adult characters
    # Step 1: extract the dropdown classes for selenium to interact with dropdown. Also extract list of character names
    # Step 2: use selenium to interact with dropdown menu and send page source back for extraction
    # Step 3: search for specific attributes with the spanID
    # Step 4: Repeat step 2 and 3 until all classes have been recorded then continue on

    # Setting up settings for selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='C:\Windows\Chromedriver\chromedriver.exe', chrome_options=options)

    characterNames = []
    dropDownId = []

    # Extracting dropdown classes and character names
    for character in regulars:
        try:
            columns = character.find_all('td')

            characterNames.append(columns[0].text)

            classes = columns[1].find_all('select')

            dropDownId.append(classes[0].get('id'))

        except Exception as e:
            print(e)
            pass

    print(characterNames)
    print(dropDownId)

    print(page)


    character = 0
    driver.get("https://serenesforest.net/awakening/characters/growth-rates/full/")
    for x in dropDownId:
        select = Select(driver.find_element_by_id(x))
        options = select.options

        for index in range(0, len(options)):
            select.select_by_index(index)
            time.sleep(0.5)
            page_source = driver.page_source
            soup2 = BeautifulSoup(page_source, 'html.parser')
            print(soup2.find(id = (characterNames[character] + '0')))

        character += 1

    driver.quit()

    return


# New item list function for FE13 taking from a different source site
def FE13ItemList():
    weaponPage = 'https://fireemblem.fandom.com/wiki/List_of_weapons_in_Fire_Emblem_Awakening'
    itemPage = 'https://fireemblem.fandom.com/wiki/List_of_items_in_Fire_Emblem_Awakening'

    try:
        rWeapon = requests.get(weaponPage)
        rItem = requests.get(itemPage)
    except:
        print('something went wrong')
        return

    overallItemList = []

    weaponSoup = BeautifulSoup(rWeapon.content, 'html.parser')
    itemSoup = BeautifulSoup(rItem.content, 'html.parser')

    weaponTable = weaponSoup.find_all('table')
    itemTable = itemSoup.find_all('table')

    for x in range(8):
        weapons = weaponTable[x].find_all('tr')

        for weapon in weapons:
            data = {
                'name' : None,
                'rank' : None,
                'range' : None,
                'uses' : None,
                'mt' : None,
                'exp' : None,
                'hit' : None,
                'crit' : None,
                'cost' : None,
                'effects' : None
            }

            nameColumn = weapon.find_all('th')
            descriptionColumn = weapon.find_all('td')

            if x == 5:
                try:
                    data['name'] = helper.GeneralUnicodeCleaner(nameColumn[1].text.rstrip())
                    data['rank'] = descriptionColumn[0].text.rstrip()
                    data['range'] = descriptionColumn[1].text.rstrip()
                    data['uses'] = int(descriptionColumn[2].text)
                    data['exp'] = int(descriptionColumn[3].text)
                    if '-' not in descriptionColumn[4].text:
                        data['cost'] = int(descriptionColumn[4].text.translate({ ord(c): None for c in'\n,'}))
                    data['description'] = descriptionColumn[5].text.rstrip()

                except Exception as e:
                    print(e)
                    pass
            elif x == 6:
                try:
                    data['name'] = helper.GeneralUnicodeCleaner(nameColumn[1].text.rstrip())
                    data['range'] = descriptionColumn[0].text.rstrip()
                    data['uses'] = int(descriptionColumn[1].text)
                    data['mt'] = int(descriptionColumn[2].text)
                    data['hit'] = int(descriptionColumn[3].text.translate({ ord(c): None for c in'%'}))
                    data['crit'] = int(descriptionColumn[4].text.translate({ ord(c): None for c in'%'}))
                    if '-' not in descriptionColumn[5].text:
                        data['cost'] = int(descriptionColumn[5].text.translate({ ord(c): None for c in'\n,'}))
                    data['description'] = descriptionColumn[5].text.rstrip()

                except Exception as e:
                    print(e)
                    pass
            elif x == 7:
                try:
                    data['name'] = helper.GeneralUnicodeCleaner(nameColumn[1].text.rstrip())
                    data['range'] = descriptionColumn[0].text.rstrip()
                    data['mt'] = int(descriptionColumn[1].text)
                    data['hit'] = int(descriptionColumn[2].text.translate({ ord(c): None for c in'%'}))
                    data['crit'] = int(descriptionColumn[3].text.translate({ ord(c): None for c in'%'}))
                    data['description'] = descriptionColumn[4].text.rstrip()

                except Exception as e:
                    print(e)
                    pass
            else:
                try:
                    data['name'] = helper.GeneralUnicodeCleaner(nameColumn[1].text.rstrip('*\n'))
                    try:
                        data['rank'] = descriptionColumn[0].find('span').attrs['title'].rstrip()
                    except:
                        data['rank'] = descriptionColumn[0].text.rstrip()
                    data['range'] = descriptionColumn[1].text.rstrip()
                    if '-' not in descriptionColumn[2].text:
                        data['uses'] = int(descriptionColumn[2].text)
                    data['mt'] = int(descriptionColumn[3].text)
                    data['hit'] = int(descriptionColumn[4].text.translate({ ord(c): None for c in'%'}))
                    data['crit'] = int(descriptionColumn[5].text.translate({ ord(c): None for c in'%'}))
                    if '-' not in descriptionColumn[6].text and 'N/A' not in descriptionColumn[6].text:
                        data['cost'] = int(descriptionColumn[6].text.translate({ ord(c): None for c in'\n,'}))
                    if len(descriptionColumn[7].text) > 3:
                        data['description'] = descriptionColumn[7].text.rstrip()

                except Exception as e:
                    print(e)
                    continue

            overallItemList.append(data)
    
    for x in range(2):
        items = itemTable[x].find_all('tr')
        
        for item in items:
            data = {
                'name' : None,
                'rank' : None,
                'range' : None,
                'uses' : None,
                'mt' : None,
                'exp' : None,
                'hit' : None,
                'crit' : None,
                'cost' : None,
                'effects' : None
            }

            nameColumn = item.find_all('th')
            descriptionColumn = item.find_all('td')

            if x == 1:
                try:
                    data['name'] = nameColumn[0].text.rstrip()
                    if '-' not in descriptionColumn[0].text:
                        data['uses'] = int(descriptionColumn[0].text.rstrip())
                    data['description'] = descriptionColumn[2].text.rstrip()
                except Exception as e:
                    print(e)
                    continue
            else:
                try:
                    data['name'] = nameColumn[0].text.rstrip()
                    if '-' not in descriptionColumn[0].text:
                        data['uses'] = int(descriptionColumn[0].text.rstrip())
                    if '-' not in descriptionColumn[1].text:
                        data['cost'] = int(descriptionColumn[1].text.translate({ ord(c): None for c in'\n*'}))
                    data['description'] = descriptionColumn[2].text.rstrip()
                except Exception as e:
                    print(e)
                    continue

            overallItemList.append(data)


    # Write information from baseGrowth into a json file
    with open('items.json', 'w') as f:
        f.write(json.dumps(overallItemList, indent=4))
        
    return