'''
Command line functionality
'''
import argparse

import vagrepo.repository

# main parser
_PARSER = argparse.ArgumentParser()
_PARSER.add_argument('--path', dest='path')
_SUBPARSERS = _PARSER.add_subparsers(dest='subcommand')
# list subcommand
_SUBPARSERS.add_parser('list', help='list available boxes')
# create subcommand
_CREATE_PARSER = _SUBPARSERS.add_parser('create', help='create new empty box')
_CREATE_PARSER.add_argument('name', metavar='NAME')
_CREATE_PARSER.add_argument('--description')
# add subcommand
_ADD_PARSER = _SUBPARSERS.add_parser('add', help='add box file to existing box')
_ADD_PARSER.add_argument('name', metavar='NAME')
_ADD_PARSER.add_argument('file', metavar='FILE')
_ADD_PARSER.add_argument('--provider')

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
        return

    mapping = {
        'list': handle_list,
        'create': handle_create,
        'add': handle_add
    }
    repository = vagrepo.repository.Repository(namespace.path)

    mapping[namespace.subcommand](namespace, repository)

def handle_list(_, repository):
    '''handle list subcommand'''
    for name in repository.box_names:
        print(name)

def handle_create(namespace, repository):
    '''handle create subcommand'''
    repository.create(namespace.name, namespace.description)

def handle_add(namespace, repository):
    '''handle add subcommand'''
    repository.add(namespace.name, namespace.file, namespace.provider)