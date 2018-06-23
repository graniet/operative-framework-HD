#!/usr/bin/env  python

from colorama import Fore, Style


class ExternalTools(object):

    def __init__(self):
        self.tools = [
            {
                'Author': 'aboul3la',
                'Name': 'Sublist3r',
                'Description': 'Fast subdomains enumeration tool for penetration testers'
            },
            {
                'Author': 'darkoperator',
                'Name': 'dnsrecon',
                'Description': 'DNS Enumeration Script'
            }
        ]

    def listing(self):
        for tool in self.tools:
            print tool['Name'] + Fore.YELLOW + ": "  + tool['Description'] + Fore.GREEN + " @" + tool['Author'] + Style.RESET_ALL
