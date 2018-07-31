import json
import os
import re
from tempfile import mkdtemp
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

    json = os.environ.get('INPUT_JSON')
    if json:
        print('INPUT_JSON: ' + json[:40])
        return json

    url = os.environ.get('INPUT_JSON_URL')
    if url:
        print('INPUT_JSON_URL: ' + url)
        return requests.get(url).text

    raise Exception('No input.json from any source')


def read_json(input_json_path, min_p_value=0):
    input_json = get_input_json(input_json_path)
    data = json.loads(input_json)
    tmp_dir = mkdtemp()
    downloads = []
    for url in data['file_relationships']:
        base = os.path.basename(urlparse(url).path)
        full = os.path.join(tmp_dir, base)
        with open(full, 'wb') as f:
            f.write(requests.get(url).content)
        downloads.append(open(full, 'rb'))
    return read_lists(downloads, min_p_value=min_p_value)


def read_lists(lists, min_p_value=0):
    '''
    Reads and filters files and returns a filename -> set dict.

    >>> from io import BytesIO
    >>> fake = BytesIO(b'id,a,p_value,z\\n42,1,2,3\\n43,4,5,6')
    >>> fake.name = '/ignore/directories/fake.txt'
    >>> lists = [fake]
    >>> filename_set_dict = read_lists(lists, min_p_value=4)
    >>> list(filename_set_dict.keys())
    ['fake.txt']
    >>> list(filename_set_dict.values())
    [{43}]
    '''
    filename_to_set = {}
    for f in lists:
        df = dataframer.parse(f).data_frame
        p_value_col = pick_col(r'p.*value', df)
        if p_value_col:
            selected_rows = df.loc[df[p_value_col] > min_p_value]
        else:
            # If we can't identify a p-value column, take the whole thing.
            selected_rows = df
        filename_to_set[os.path.basename(f.name)] = \
            set(selected_rows.index.tolist())
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
