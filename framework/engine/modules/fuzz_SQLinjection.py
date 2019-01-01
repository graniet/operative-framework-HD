#!/usr/bin/env	python
#description:	Fuzz link to discover generic SQL injection#

import os
import string
import random
import json
import subprocess

class module_element(object):

    def __init__(self):
        self.title = "SQLi Generic fuzzer : \n"
        self.require = [
            {"name": "link", "value": "", "required": "yes"}
        ]
        self.export = []
        self.id_list = []
        self.export_file = ""
        self.export_status = False
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'link',
            'result': "rows",
            'export_primary': 'vulnerability',
            'description': 'Fuzz link to discover generic SQL injection'
        }
        self.fuzzing = [
            '1 or 1=1',
            "1' or '1'='1",
            "1'or'1'='1",
            "'",
            "'1"
        ]

    def get_options(self, name):
        for argument in self.require:
            if argument['name'] == name:
                return argument['value']

    def generate_unique_id(self, size=6, chars=string.ascii_uppercase + string.digits):
        start = 0
        unique_id = ""
        while start == 0:
            unique_id = ''.join(random.choice(chars) for _ in range(size))
            if unique_id not in self.id_list:
                self.id_list.append(unique_id)
                start = 1
        return unique_id

    def main(self):
        vulnerability_checked = []
        vulnerability = []
        link = self.get_options('link')
        if "://" not in link:
            link = "http://" + link
        directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 2)[0]
        res = subprocess.Popen(['/usr/bin/python', directory + '/external_tool/DSSS/dsss.py', '-u', link],
                              stdout=subprocess.PIPE)
        output = res.stdout.read()
        print link
        test_out = json.loads(output)
        for element in test_out:
            if element['vulnerability'] not in vulnerability_checked:
                vulnerability.append({
                    '_id': self.generate_unique_id(),
                    'vulnerability': element['vulnerability']
                })
                vulnerability_checked.append(element['vulnerability'])
        self.export.append(vulnerability)


