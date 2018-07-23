import requests
import os
import json
import argparse
import pathlib

from sets import Sets


def arg_parser():
    parser = argparse.ArgumentParser(
        description='A variety of set intersection visualizations')

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--json', type=str,
        help='If given file does not exist, fall back to environment variable')
    group.add_argument(
        '--lists', nargs='+', type=argparse.FileType('r'),
        help='Single column lists')

    parser.add_argument(
        '--output', type=str,
        help='Destination directory')

    return parser


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


def read_json(input_json_path):
    input_json = get_input_json(input_json_path)
    data = json.loads(input_json)
    return {
        os.path.basename(url): {
            l.strip() for l in requests.get(url).text.split('\n')
        } for url in data['file_relationships']
    }


def read_lists(lists):
    return {os.path.basename(f.name) : {l.strip() for l in f.readlines()}
            for f in lists}


if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    if args.json:
        lists = read_json(args.json)
    elif args.lists:
        lists = read_lists(args.lists)
    else:
        raise Exception('Either --json or --lists should be given')
    sets = Sets(lists)
    pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)
    sets.print_columns(os.path.join(args.output, 'columns.txt'))
    sets.print_ratio_matrix(os.path.join(args.output, 'ratio_matrix.txt'))

