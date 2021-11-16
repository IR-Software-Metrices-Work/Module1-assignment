import pandas as pd
import string
import requests as requests
from bs4 import BeautifulSoup
import numpy as np
import re

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

def along_side_with_java() :
    lang = [['java'], ['python'], ['c'], ['kotlin'], ['swift'], ['rust'], ['ruby'], ['scala'], ['julia'], ['lua']]
    parsed_description = parse_job_description()
    parsed_db = parse_db()
    all_terms = lang + parsed_db
    query_map = pd.DataFrame(parsed_description.apply(
        lambda s: [1 if np.all([d in s for d in db]) else 0 for db in all_terms]).values.tolist(),
        columns=[' '.join(d) for d in all_terms])

    output = query_map[query_map['java'] > 0].apply(lambda s: np.where(s == 1)[0], axis=1).apply(lambda s: list(query_map.columns[s]))
    print(output)


def along_side_with_python():
    lang = [['python'],['java'], ['c'], ['kotlin'], ['swift'], ['rust'], ['ruby'], ['scala'], ['julia'], ['lua'],['.net'],['c#'],['dart'],['flutter']]
    parsed_description = parse_job_description()
    query_map = pd.DataFrame(
        parsed_description.apply(
            lambda s: [
                1 if np.all([d in s for d in db])
                else 0 for db in lang]
            ).values.tolist(),
        columns=[' '.join(d) for d in lang]
    )

    output = query_map[query_map['python'] > 0].apply(
        lambda s: np.where(s == 1)[0], axis=1).apply(
        lambda s: list(query_map.columns[s])
    )

    output_no_duplicates = query_map[query_map['python'] > 0].apply(
        lambda s: np.where(s == 1)[0], axis=1).apply(
        lambda s: list(query_map.columns[s])
    ).drop_duplicates()

    show_data(output,output_no_duplicates)

def alongside_with_oracle():
    parsed_description = parse_job_description()
    parsed_db = parse_db()
    query_map = pd.DataFrame(
        parsed_description.apply(
            lambda s: [
                1 if np.all([d in s for d in db])
                else 0 for db in parsed_db]
            ).values.tolist(),
        columns=[' '.join(d) for d in parsed_db]
    )

    output = query_map[query_map['oracle'] > 0].apply(
        lambda s: np.where(s == 1)[0], axis=1).apply(
        lambda s: list(query_map.columns[s])
    )

    output_no_duplicates = query_map[query_map['oracle'] > 0].apply(
        lambda s: np.where(s == 1)[0], axis=1).apply(
        lambda s: list(query_map.columns[s])
    ).drop_duplicates()

    show_data(output,output_no_duplicates)



def show_data(output,output_no_duplicates) :
    summary_map = pd.DataFrame(
        output.apply(
            lambda s: [
                1 if np.all([d in s for d in db])
                else 0 for db in output_no_duplicates]
        ).values.tolist(),
        columns=[' '.join(d) for d in output_no_duplicates]
    )
    print(summary_map)
    for item in output_no_duplicates:
        col = ''
        for i in item:
            col += i + ' '
        col = re.sub(r"\s+$", "", col)
        print(col, ":", summary_map[col].values.sum(), 'of', output.size)