import json
import os
import re
from io import BytesIO
from urllib.parse import urlparse

import requests
from dataframer import dataframer


def get_input_json(possible_input_file):
    '''
    Checks three possible sources for JSON input,
    and returns JSON string if found.
    Returns None if all three fail.
    '''
    if os.path.isfile(possible_input_file):
        return open(possible_input_file, 'r').read(None)

    url = os.environ.get('INPUT_JSON_URL')
    if url:
        print('INPUT_JSON_URL: ' + url)
        return requests.get(url).text

    json = os.environ.get('INPUT_JSON')
    if json:
        print('INPUT_JSON: ' + json[:40])
        return json

    raise Exception('No input.json from any source')


def read_json(input_json_path):
    input_json = get_input_json(input_json_path)
    data = json.loads(input_json)
    streams = []
    for url in data['file_relationships']:
        bytes = requests.get(url).content
        stream = BytesIO(bytes)
        stream.name = os.path.basename(urlparse(url).path)
        streams.append(stream)
    for parameter in data['parameters']:
        if parameter['name'] == 'p-value bound':
            p_value_bound = parameter['value']
        if parameter['name'] == 'fold-change bound':
            fold_change_bound = parameter['value']
        if parameter['name'] == 'fold-change increase':
            fold_change_is_increase = parameter['value']
    return read_files(streams, p_value_bound=p_value_bound,
                      fold_change_bound=fold_change_bound,
                      fold_change_is_increase=fold_change_is_increase)


def read_files(files, p_value_bound=None,
               fold_change_bound=None, fold_change_is_increase=None):
    '''
    Reads and filters files and returns a filename -> set dict.

    >>> from io import BytesIO
    >>> file = BytesIO('\\n'.join([ \
                'id,p_value,fold_change', \
                'id00,0,0', \
                'id11,1,1', \
                'id22,2,2', \
                'id02,0,2', \
                'id20,2,0']).encode('utf-8'))
    >>> file.name = '/ignore/directories/fake.txt'
    >>> lists = [file]

    # No filters:
    >>> selected = read_files(lists)
    >>> list(selected.keys())
    ['fake.txt']
    >>> sorted(list(selected.values())[0])
    ['id00', 'id02', 'id11', 'id20', 'id22']

    # p-value:
    >>> selected = read_files(lists, p_value_bound=1)
    >>> sorted(list(selected.values())[0])
    ['id00', 'id02']

    # fold-change increase:
    >>> selected = read_files(lists, fold_change_bound=1, \
                    fold_change_is_increase=True)
    >>> sorted(list(selected.values())[0])
    ['id02', 'id22']

    # fold-change decrease:
    >>> selected = read_files(lists, fold_change_bound=1, \
                    fold_change_is_increase=False)
    >>> sorted(list(selected.values())[0])
    ['id00', 'id20']

    # p-value and fold-change increase:
    >>> selected = read_files(lists, p_value_bound=1, fold_change_bound=1, \
                    fold_change_is_increase=True)
    >>> sorted(list(selected.values())[0])
    ['id02']

    '''
    filename_to_set = {}
    for f in files:
        df = dataframer.parse(f).data_frame

        p_value_col = pick_col(r'p.*value', df)
        if p_value_col and p_value_bound is not None:
            df_p_value_filtered = df.loc[df[p_value_col] < p_value_bound]
        else:
            # If we can't identify a p-value column, take the whole thing.
            df_p_value_filtered = df

        fold_change_col = pick_col(r'fold.*change', df)
        if fold_change_col and fold_change_bound is not None:
            filter = (df[fold_change_col] > fold_change_bound) \
                if fold_change_is_increase \
                else (df[fold_change_col] < fold_change_bound)
            df_fold_change_filtered = df_p_value_filtered.loc[filter]
        else:
            # If we can't identify a fold-change column, take the whole thing.
            df_fold_change_filtered = df_p_value_filtered

        filename_to_set[os.path.basename(f.name)] = \
            set(df_fold_change_filtered.index.tolist())
    return filename_to_set


def pick_col(name_re, df):
    '''
    Picks single column from dataframe that matches given name_re.

    >>> import pandas
    >>> df = pandas.DataFrame(
    ...  columns=['a', 'P Value', 'z'],
    ...  data=[[1, 2, 3]]
    ... )
    >>> pick_col(r'p.*val', df)
    'P Value'

    '''
    match_cols = [
        col for col in df.columns
        if re.search(name_re, col, flags=re.IGNORECASE)
    ]
    assert len(match_cols) <= 1, \
        'expected one match for /{}/i in {}, got {}'.format(
            name_re, df.columns.tolist(), match_cols
    )
    if len(match_cols) == 1:
        return match_cols[0]
    return None
