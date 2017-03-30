'''
Command line functionality
'''
import argparse

import vagrepo.repository

_PARSER = argparse.ArgumentParser()
_PARSER.add_argument('--path', dest='path')

_SUBPARSERS = _PARSER.add_subparsers(dest='subcommand')
_SUBPARSERS.add_parser('list', help="list available boxes")

def parse_args():
    '''Create configured parser instance'''
    return _PARSER.parse_args()

def print_help():
    '''Print command line help message'''
    _PARSER.print_help()

def handle(namespace):
    '''
    handle parsed command line arguments, route call to correct subcommand
    handler function
    '''
    if namespace.subcommand is None:
        print_help()
    else:
        repository = vagrepo.repository.Repository(namespace.path)
        handle_list(namespace, repository)

def handle_list(_, repository):
    '''handle command line list subcommand'''
    for name in repository.box_names:
        print(name)
