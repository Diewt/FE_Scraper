import re

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

def NameCleaner(data):
    if '\u2019' in data['name']:
        data['name'] = data['name'].replace('\u2019', '\'')

    return data



