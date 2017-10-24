
import argparse
import sys

from . import generate_schemas

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate JSON schema files for the Riot Games API')
    parser.add_argument('-o', '--output', dest='out', default='gen/', help='directory to save schema files in')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')

    args = parser.parse_args()

    generate_schemas(args.out, verbose=args.verbose)
