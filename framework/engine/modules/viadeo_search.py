#!/usr/bin/env	python
# -*- coding: utf-8 -*-
#description:Viadeo employee search module#

import os
import sys
import urllib
import re
import string
import requests
import random

class module_element(object):
    def __init__(self):
        self.title = "Viadeo gathering : \n"
        self.require = [
            {
                "name": "enterprise",
                "placeholder": "enterprise name",
                "value": "",
                "required": "yes"
            },
            {
                "name": "limit",
                "placeholder": "limit result",
                "value": "100",
                "required": "no"
            }
        ]
        self.export = []
        self.export_file = ""
        self.export_status = False
        self.id_list = []
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'enterprise',
            'result': "rows",
            'export_primary': 'employee',
            'description': 'Search possible employees list on Viadeo.com'
        }

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
        server = "www.google.fr"
        limit = 100
        employee = []
        if self.get_options('limit') != '':
            limit = int(self.get_options('limit'))
        url = "http://"+server+"/search?num="+str(limit)+"&start=10&hl=en&meta=&q=site%3Afr.viadeo.com/fr/profile/%20"+self.get_options('enterprise')
        r = requests.get(url)
        results = r.content
        regex = re.compile("\>fr\.viadeo\.com\/fr\/profile\/(.*?)\<\/cite")
        output = regex.findall(results)
        if len(output) > 0:
            for line in output:
                if line.strip() != "":
                    employee.append({
                        "employee": line.strip().decode('latin-1').encode("utf-8"),
                        "employee_link": "https://fr.viadeo.com/fr/profile/" + line.strip().decode('latin-1').encode("utf-8"),
                        "_id": self.generate_unique_id()
                    })
            self.export.append(employee)
            return True
        else:
            return False


