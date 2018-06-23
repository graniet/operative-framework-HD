#!/usr/bin/env	python

import os
import json
import string
import random
import subprocess


class module_element(object):

    def __init__(self):
        self.require = [
            {"name": "website", "value": "", "required": "yes", "placeholder": "https://linkedin.com"},
            {"name": "dnsrecon_arguments", "value": "", "required": "no", "placeholder": "ex: -a,--iw..."}
        ]
        self.id_list = []
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'result': "rows",
            'export_primary': 'record',
            'description': 'Standard DNS enumeration'
        }
        self.export = []

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
        dns_tpl = []
        website = self.get_options('website')
        arguments = self.get_options('dnsrecon_arguments')
        if "," in arguments:
            arguments = arguments.split(',')
        website = website.split("//")[-1].split("/")[0].split('?')[0]
        directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 2)[0]
        if "www." in website:
            website = website.split('www.')[1]
        if len(arguments) > 0:
            res = subprocess.Popen(['/usr/bin/python', directory + '/external_tool/dnsrecon/execute.py', '-d', website, '-j', directory + '/external_tool/dnsrecon/JSON2' , arguments],
                               stdout=subprocess.PIPE)
        else:
            res = subprocess.Popen(
                ['/usr/bin/python', directory + '/external_tool/dnsrecon/execute.py', '-d', website, '-j', directory + '/external_tool/dnsrecon/JSON2'],
                stdout=subprocess.PIPE)
        output = res.stdout.read()
        if os.path.isfile(directory + '/external_tool/dnsrecon/JSON2'):
            json_file = open(directory + '/external_tool/dnsrecon/JSON2').read()
            json_txt = json.loads(json_file)
            for element in json_txt:
                tpl = {}
                if "type" in element:
                    if str(element['type']) == "ScanInfo":
                        continue
                    tpl['type'] = str(element['type'])
                else:
                    tpl['type'] = "no type"
                if "address" in element:
                    tpl['address'] = str(element['address'])
                else:
                    tpl['address'] = "no address"
                if "target" in element:
                    tpl['target'] = str(element['target'])
                else:
                    tpl['target'] = "no target"
                if "port" in element:
                    tpl['port'] = str(element['port'])
                else:
                    tpl['port'] = "no port"
                if "name" in element:
                    tpl['name'] = str(element['name'])
                else:
                    tpl['name'] = "no name"
                if "exchange" in element:
                    tpl['exchange'] = str(element['exchange'])
                else:
                    tpl['exchange'] = "no exchange"
                tpl['_id'] = self.generate_unique_id()
                dns_tpl.append(tpl)
            self.export.append(dns_tpl)





