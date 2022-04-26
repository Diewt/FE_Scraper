import re

# Helper function to clean up unicode values found in the data
def FE13SkillCleaner(data, skillType):

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

    if skillType == 1:
        if data['class'] == "\u2013":
            data['class'] = '-'

        if data['level'] == "\u2013":
            data['level'] = '-'

    data = FE13SkillNotes(data, skillType)

    return data

# Helper Function to add in notes from the site scraped
def FE13SkillNotes(data, skillType):
    # skillType 1 is obtainable skills, skillType 2 is enemy only skills
    if skillType == 1:
        # Note 1
        if '*1' in data['effect']:
            data['effect'] = data['effect'].replace('*1', '(Strenght, Magic, Skill, Speed, Luck, Defense, Resistance)')
        # Note 2
        if '*2' in data['effect']:
            data['effect'] = data['effect'].replace('*2', '(Does not apply for Dual Strikes)')
        # Note 3
        if '*3' in data['effect']:
            data['effect'] = data['effect'].replace('*3', '(Horse, Pegasus, Griffon riders, and Taguel')
        # Note 4
        if '*4' in data['effect']:
            data['effect'] = data['effect'].replace('*4', '(DLC only)')
        if '*4' in data['class']:
            data['class'] = data['class'].replace('*4', '(DLC only)')
        
    elif skillType == 2:
        # Note 1
        if '*1' in data['effect']:
            data['effect'] = data['effect'].replace('*1', '(Does not apply for Dual Strikes)')

    return data

# Helper function to clean up unicode values found in the data
def NameCleaner(data):
    if '\u2019' in data['name']:
        data['name'] = data['name'].replace('\u2019', '\'')

    return data

def GeneralUnicodeCleaner(data):
    try:
        if '\u2019' in data:
            data = data.replace('\u2019', '\'')
        if "\u2013" in data:
            data = data.replace('\u2013', '-')
        if '\u00f6' in data:
            data = data.replace('\u00f6', 'o')
        if '\u00e1' in data:
            data = data.replace('\u00e1', 'a')
        if '*' in data:
            data.translate({ ord(c): None for c in'*'})
    except Exception as e:
        print(e)
        return data

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


