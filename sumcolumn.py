#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(
    description="Output the sum of integers in a given column")
parser.add_argument(
    dest='filename', default='/dev/stdin',
    help='file to read, specify - to read from stdin')
parser.add_argument(
    '-c', '--column=', dest='column', action='store', type=int, default=0,
    help='select this column instead of column 0')
parser.add_argument(
    '-d', '--delimiter=', dest='delimiter', action='store', default=' ',
    help='use this delimiter instead of whitespace to separate columns')
args = parser.parse_args()

if args.filename == '-':
    args.filename = '/dev/stdin'
total = 0
with open(args.filename) as f:
    for line in f:
        cols = line.split(args.delimiter)
        total += int(cols[args.column])
print(total)
