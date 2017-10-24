
import json
import os
import re

import requests

from . import ApiRefPageParser


def generate_schemas(output_directory, verbose=False):
    apis = [
        'champion-mastery-v3',
        'champion-v3',
        'league-v3',
        'lol-static-data-v3',
        'lol-status-v3',
        'masteries-v3',
        'match-v3',
        'runes-v3',
        'spectator-v3',
        'summoner-v3',
    ]

    for api in apis:
        parser = ApiRefPageParser()
        ref_page = requests.get('https://developer.riotgames.com/api-details/{}'.format(api))

        parser.feed(ref_page.json()['html'])

        if verbose:
            print('{}: found these types:'.format(api))

            for t in set(parser.types):
                print('\n\ttypename: {}\n\tcomment: {}\n\tproperties:'.format(t.typename, t.comment))

                for p in t.properties:
                    print('\n\t\tname: {}\n\t\ttype: {}\n\t\tcomment: {}'.format(p.name, p.typename, p.comment))
                
                print('\n')
        
        for t in set(parser.types):
            transformed = {
                '$schema': 'http://json-schema.org/draft-06/schema#',
                'title': t.typename,
                'description': t.comment,
                'type': 'object',
                'properties': {}
            }

            for p in t.properties:
                prop_def = property_type_definition(p.typename)
                prop_def['description'] = p.comment
                transformed['properties'][p.name] = prop_def

            os.makedirs('{}/{}'.format(output_directory, api), exist_ok=True)
            with open('{}/{}/{}.schema.json'.format(output_directory, api, t.typename), 'w') as f:
                json.dump(transformed, f, indent=4, sort_keys=True)

def is_basic_type(typename):
    return (typename == 'string' or
            typename == 'boolean' or
            typename == 'number' or
            typename == 'array' or
            typename == 'object' or
            typename == 'null' or
            typename == 'integer')

def property_type_definition(property_name):
    if property_name == 'int' or property_name == 'long':
        property_name = 'integer'
    elif property_name == 'double':
        property_name = 'number'

    list_match = re.search(r'(List|Set)\[(\w+)\]', property_name)
    dict_match = re.search(r'Map\[(\w+), (\w+)\]', property_name)

    if list_match is not None:
        return {
            'type': 'array',
            'items': property_type_definition(list_match.group(2)),
            'uniqueItems': list_match.group(1) == 'Set'
        }
    elif dict_match is not None:
        if dict_match.group(1) != 'string':
            print('found Map with key other than string!! schema may be invalid. {}'.format(property_name))
        return {
            'type': 'object',
            'additionalProprties': property_type_definition(dict_match.group(2))
        }
    elif not is_basic_type(property_name):
        return {
            '$ref': '{}.schema.json#'.format(property_name)
        }
    else:
        return {
            'type': property_name
        }
