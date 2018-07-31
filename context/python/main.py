#!/usr/bin/env python

import argparse
import os
import pathlib
from sets import Sets

from parse import read_json, read_lists


def arg_parser():
    parser = argparse.ArgumentParser(
        description='A variety of set intersection visualizations')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--json', type=str,
        help='If given file does not exist, fall back to environment variable')
    group.add_argument(
        '--lists', nargs='+', type=argparse.FileType('rb'),
        help='Single column lists')

    parser.add_argument(
        '--output', type=str, required=True,
        help='Destination directory')

    return parser


if __name__ == '__main__':
    parser = arg_parser()
    args = parser.parse_args()
    if args.json:
        lists = read_json(args.json)
    elif args.lists:
        lists = read_lists(args.lists)
    else:
        raise Exception('argparse validation should have failed earlier')
    sets = Sets(lists)
    pathlib.Path(args.output).mkdir(parents=True, exist_ok=True)
    sets.print_columns(os.path.join(args.output, 'columns.txt'))
    sets.print_ratio_matrix(os.path.join(args.output, 'ratio_matrix.txt'))
