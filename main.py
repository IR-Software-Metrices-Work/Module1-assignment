import pandas as pd
import string
import requests as requests
from bs4 import BeautifulSoup
import numpy as np

def get_and_clean_data():
    data = pd.read_csv('data/software_developer_united_states_1971_20191023_1.csv')
    description = data['job_description']
    cleaned_description = description.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_description = cleaned_description.apply(lambda s: s.lower())
    cleaned_description = cleaned_description.apply(lambda s: s.translate(str.maketrans(string.whitespace, ' '*len(string.whitespace), '')))
    cleaned_description = cleaned_description.drop_duplicates()
    return cleaned_description

def simple_tokenize(data) :
    cleaned_description = data.apply(lambda s: [x.strip() for x in s.split()])
    return cleaned_description

def parse_job_description():
    cleaned_description = get_and_clean_data()
    cleaned_description = simple_tokenize(cleaned_description)
    return cleaned_description

def parse_db():
    html_doc = requests.get("https://www.improgrammer.net/top-10-databases-should-learn-2015/").content
    soup = BeautifulSoup(html_doc, 'html.parser')
    all_db = [s.get_text() for s in soup.findAll('dt')]
    db_list = [s.lower() for s in all_db]
    db_list = [[x.strip() for x in s.split()] for s in db_list]
    return db_list

def to_percent(a,b):
    return str(round((100/b) * a, 2))

def database_after_java() :
    parsed_db = parse_db()
    parsed_description = parse_job_description()
    with_java = [None] * len(parsed_db)
    counted_db = [None] * len(parsed_db)
    for i, db in enumerate(parsed_db):
        with_java[i] = parsed_description.apply(lambda s: np.all([x in s for x in db]) and 'java' in s).sum()
        counted_db[i] = parsed_description.apply(lambda s: np.all([x in s for x in db])).sum()
        percent = to_percent(with_java[i], counted_db[i])
        print(' '.join(db) + ' + java: ' + str(with_java[i]) + ' of ' + str(counted_db[i]) + ' (' + percent + '%)')

# todo

# What DB should I learn after java? done :
# I wound say I will learn db2 after finish java because of the demand in the market

# Which DB is in demand alongside oracle?

# What programing language is in demand alongside python?

# Create a 0-1 vector using bitwise and/or
# Start with something like: