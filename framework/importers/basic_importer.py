#!/usr/bin/env  python

import os
from importer_base import OpfBaseImporter
from colorama import Fore, Style


class OpfImporter(OpfBaseImporter):

    def __init__(self):
        OpfBaseImporter.__init__(self)
        self.meta = {
            'author': 'Tristan Granier',
            'description': 'Basic importer for text file.'
        }
        self.error_message = ''
        self.arguments = [
            {'name': 'filename', 'required': 'yes', 'value': ''},
            {'name': 'separator', 'required': 'yes', 'value': ':'},
            {'name': 'extraction_base', 'required': 'yes', 'value': 'email:password'}
        ]

    def run(self):
        collection = self.database.public_breach
        collection_searchable = self.database.public_breach_searchable
        if not self.check_argument(self.arguments):
            self.set_error("Argument required empty")
            return False
        breach_file = str(self.get_argument('filename', self.arguments))
        search = collection.find({'breach_name': breach_file}, {'_id': False})
        if search.count() > 1:
            self.set_error("Filename as already added to database.")
            return False
        if not os.path.isfile(breach_file):
            self.set_error("This file as been not found, please use complet path like: '/home/root/file.txt'.")
            return False
        separator = str(self.get_argument('separator', self.arguments))
        extraction_base = self.get_argument('extraction_base', self.arguments)
        if not separator in extraction_base:
            self.set_error("Don't find separator in extraction_base, if you use : separator please set extraction_base like: 'email:pass'")
            return False
        num_lines = sum(1 for line in open(breach_file))
        if num_lines < 2:
            self.set_error('This is empty please select another file.')
            return False
        breach_id = self.random_breach()
        collection.insert({'breach_id': breach_id, 'breach_file': breach_file, 'created_at': str(self.get_date()), 'updated_at': str(self.get_date())})
        extraction_base = extraction_base.split(separator)
        for element in extraction_base:
            if collection_searchable.find({'searchable': str(element).strip()}).count() < 1:
                collection_searchable.insert({'breach_id': breach_id,'searchable':str(element).strip(),  'breach_file': breach_file, 'created_at': str(self.get_date()), 'updated_at': str(self.get_date())})
        collection_breach = self.database.public_breach_content
        nb = 0
        with open(breach_file) as f:
            nb = nb + 1
            for line in f:
                breach_content_id = self.random_breach_content()
                if separator in line:
                    line = line.split(separator)
                    for key, value in enumerate(extraction_base):
                        if line[key]:
                            select = collection_breach.find({'breach_file': breach_file, str(value).strip(): str(line[key]).strip()})
                            if select.count() < 1:
                                try:
                                    print Fore.BLUE + "=> " + Style.RESET_ALL + str(line[key]).strip() + " ("+str(value).strip()+")"
                                    collection_breach.insert({'breach_content_id': breach_content_id, str(value).strip(): str(line[key]).strip(), 'created_at': str(self.get_date()), 'updated_at': str(self.get_date()), 'breach_file': breach_file})
                                except:
                                    error = 1
        print Fore.GREEN + "=> " + Style.RESET_ALL + str(nb) + " imported."
        return True


