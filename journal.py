# -*- coding: utf-8 -*-
import argparse
from lib2to3.pytree import Base
import os
from params import Params
import json

'''
input:
    path:path of the entry data
return:
    dictionary
'''
def load_json(path):
    data = None
    try:
        f = open(path)
        raw_data = f.read()
        data = json.loads(raw_data)
    except BaseException as e:
        print(e)
    return data

'''
input: 
    data: dictionary
    path: path of the entry data
return: 
    boolean - whether the operation is successful or not
'''
def dump_json(data, path):
    try:
        data_str = json.dumps(data)
        f = open(path, 'w')
        f.write(data_str)
    except BaseException as e:
        print(e)
        return False


class Journal:
    def __init__(self):
        self.params = Params()
        self.data = None
        
    def format_journal(self, content):
        return {
            "content" : content,
        }
        
    def create_journal(self, content, title):
        if self.data == None:
            self.data = load_json(self.params.data_path)
            if self.data == None:
                return False

        if title in self.data:
            print("Journal has been created!")
            return False

        #open a file with name title and store the content
        entry = self.format_journal(content)
        self.data[title] = entry
        if not dump_json(self.data, self.params.data_path):
            return False
        
        return True

    def list_journal(self):
        return self.data.key()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Journal System')
    parser.add_argument('--create',  '-c', type=str,
                        help='create a journal')
    parser.add_argument('--title',  '-t', type=str,
                        help='title of the journal, use with create')

    parser.add_argument('--list', '-l', action='store_true',
                        help='list of the titles of all of the entries')

    args = parser.parse_args()
    journal = Journal()
    if args.create:
        if not args.title:
            print("You need a title for the journal!")
        else:
            journal.create_journal(args.create, args.title)

    elif args.list:
        journal.list_journal()
