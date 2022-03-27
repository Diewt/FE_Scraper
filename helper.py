import re

# Helper function to clean up unicode values found in the data
def FE13SkillCleaner(data):

    if data['activation'] == "\u2013":
        data['activation'] = '-'

    if '\n\t\t\t' in data['effect']:
        data['effect'] = data['effect'].replace('\n\t\t\t', '')
        data['effect'] = re.sub(' +', ' ', data['effect'])

    if '\u2019' in data['effect']:
        data['effect'] = data['effect'].replace('\u2019', '\'')

    if "\u2013" in data['effect']:
        data['effect'] = data['effect'].replace('\u2013', '-')

    if '\u2019' in data['skill']:
        data['skill'] = data['skill'].replace('\u2019', '\'')

    try:
        if data['class'] == "\u2013":
            data['class'] = '-'

        if data['level'] == "\u2013":
            data['level'] = '-'
    except:
        pass

    return data

# Helper function to clean up unicode values found in the data
def NameCleaner(data):
    if '\u2019' in data['name']:
        data['name'] = data['name'].replace('\u2019', '\'')

    return data

# Function to set up the data into a dictionary that will be sent back
def FE13baseGrowthData(columns):
    data = {
        'name' : columns[0].text,
        'hp' : int(columns[1].text),
        'str' : int(columns[2].text),
        'mag' : int(columns[3].text),
        'skl' : int(columns[4].text),
        'spd' : int(columns[5].text),
        'lck' : int(columns[6].text),
        'def' : int(columns[7].text),
        'res' : int(columns[8].text)
    }

    # Clean up any unicode data
    NameCleaner(data)

    # Return dictionary data back to call
    return data

# Function to set up a dictionary for weapons that will be sent back
def FE13weaponData(columns):
    # Using Try Statement to account for any mismatching values ie. (encountering - for value normally has number value)
    try:
        data = {
            'name' : columns[1].text,
            'rank' : columns[2].text,
            'mt' : int(columns[3].text),
            'hit' : int(columns[4].text),
            'crit' : int(columns[5].text),
            'rng' : columns[6].text,
            'effect' : '',
            'uses' : columns[8].text,
            'worth' : columns[9].text,
            'description' : columns[10].text
        }
    except ValueError:
            data = {
            'name' : columns[1].text,
            'rank' : columns[2].text,
            'mt' : int(columns[3].text),
            'hit' : int(columns[4].text),
            'crit' : int(columns[5].text),
            'rng' : columns[6].text,
            'effect' : '',
            'uses' : columns[8].text,
            'worth' : columns[9].text,
            'description' : columns[10].text
        }

    return data

# Function to set up a dictionary for use items that will be sent back
def FE13useItemData(columns):
    
    # Using Try Statement to account for any mismatching values ie. (encountering - for value normally has number value)
    try:
        data = {
            'name' : columns[1].text,
            'uses' : int(columns[2].text),
            'worth' : int(columns[3].text),
            'description' : columns[4].text
        }
    except ValueError:
        data = {
            'name' : columns[1].text,
            'uses' : columns[2].text,
            'worth' : columns[3].text,
            'description' : columns[4].text
        }
        
    return data

