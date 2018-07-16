import requests
import os
import json
import argparse


def get_input_json(possible_input_file):
    '''
    Checks three possible sources for JSON input,
    and returns JSON string if found.
    Returns None if all three fail.
    '''
    if possible_input_file and os.path.isfile(possible_input_file):
        return open(possible_input_file, 'r').read(None)

    json = os.environ.get('INPUT_JSON')
    if json:
        return json

    url = os.environ.get('INPUT_JSON_URL')
    if url:
        print('url: ' + url)
        return requests.get(url).text

    return None

def load(input_json_path):
    input_json = get_input_json(input_json_path)
    if input_json:
        data = json.loads(input_json)
        strings = [requests.get(url).text for url in data['file_relationships']]
        sets = []

def arg_parser():
    parser = argparse.ArgumentParser(
        description='A variety of set intersection visualizations')

    parser.add_argument(
        '--json', nargs='?', type=argparse.FileType('r'),
        help='input.json')
    parser.add_argument(
        '--lists', nargs='+', type=argparse.FileType('r'),
        help='Single column lists')

    return parser

def read_lists(lists):
    return {os.path.basename(f.name) : {l.strip() for l in f.readlines()} for f in lists}

if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    if args.json:
        raise StandardError('TODO')
    elif args.lists:
        lists = read_lists(args.lists)
        print(lists)
