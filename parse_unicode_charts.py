import requests
from bs4 import BeautifulSoup

FIXES = {
    'Latin': 'Basic Latin',
    'Greek': 'Greek and Coptic',
    'CJK Unified Ideographs (Han) (35MB)': 'CJK Unified Ideographs',
    'CJK  Extension A (6MB)': 'CJK Unified Ideographs Extension A',
    'CJK Extension B (40MB)': 'CJK Unified Ideographs Extension B',
    'CJK Extension C (3MB)': 'CJK Unified Ideographs Extension C',
    'CJK Extension D': 'CJK Unified Ideographs Extension D',
    'CJK Extension E (3.5MB)': 'CJK Unified Ideographs Extension E',
    'CJK Extension F (4MB)': 'CJK Unified Ideographs Extension F',
    'CJK Extension G (2MB)': 'CJK Unified Ideographs Extension G',
    'CJK Extension H (2.5MB)': 'CJK Unified Ideographs Extension H',
    "N'Ko": 'NKo',
    'CJK Radicals / Kangxi Radicals': 'Kangxi Radicals',
    'Oriya (Odia)': 'Oriya',
    'Bengali and Assamese': 'Bengali',
    'Phags-Pa': 'Phags-pa',
    'Aramaic, Imperial': 'Imperial Aramaic',
    'Pahlavi, Inscriptional': 'Inscriptional Pahlavi',
    'Pahlavi, Psalter': 'Psalter Pahlavi',
    'Parthian, Inscriptional': 'Inscriptional Parthian',
    'Optical Character Recognition (OCR)': 'Optical Character Recognition',
    'Super and Subscripts': 'Superscripts and Subscripts',
    'Miscellaneous Symbols And Pictographs': 'Miscellaneous Symbols and Pictographs',
}

IGNORE = [
    'Armenian Ligatures',
    'Basic Latin (ASCII)',
    'Coptic in Greek block',
    '(see also Unihan Database)',
    'ASCII Punctuation',
    'Latin-1 Punctuation',
    'Roman Symbols',
    'Additional Squared Symbols',
    'ASCII Digits',
    'Fullwidth ASCII Digits',
    'Basic operators: Plus, Factorial, Division, Multiplication',
    'Additional Shapes',
    '(see also specific scripts)',
    'Dollar Sign, Euro Sign',
    'Yen, Pound and Cent',
    'Fullwidth Currency Symbols',
    'Rial Sign',
    'Chess, Checkers/Draughts',
    'Yijing Mono-, Di- and Trigrams',
]


def print_blocklist(table):
    block_list = {}
    sg = None
    mb = None
    sg_list = []
    mb_list = []
    for p in table.find_all('p'):
        value = p.text.strip().replace('\xa0', ' ')
        if value in IGNORE:
            continue
        if value in FIXES.keys():
            value = FIXES[value]

        if p['class'][0] == 'sg':
            if sg:
                if mb:
                    sg_list.append({mb: mb_list})
                block_list[sg] = sg_list
            sg_list = []
            mb_list =[]
            sg = value
            mb = None
        elif p['class'][0] == 'mb':
            if mb:
                sg_list.append({mb: mb_list})
            mb = value
            mb_list =[]
        elif p['class'][0] == 'pb':
            mb_list.append(value)
        elif p['class'][0] == 'sb':
            if mb:
                sg_list.append({mb: mb_list})
            mb_list =[]
            mb = None
            sg_list.append({value: []})

    print(block_list)

url = 'https://www.unicode.org/charts/index.html'

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'html.parser')

scripts_table = soup.find('table', {'id': 'table5'})
symbols_table = soup.find('table', {'id': 'table9'})

print_blocklist(scripts_table)
print('\n')
print_blocklist(symbols_table)
