#!/usr/bin/env	python
#description:Extract url for website domain#

from colorama import Fore,Back,Style
from bs4 import BeautifulSoup

import os,sys
import time
import string
import random
import requests

class module_element(object):
    def __init__(self):
        self.title = "Website Url gathering : \n"
        self.require = [
            {"name": "website", "value": "", "required": "yes"},
            {"name": "page_limit", "value": "100", "required": "no"}
        ]
        self.export = []
        self.export_file = ""
        self.export_status = False
        self.already = []
        self.id_list = []
        self.linked = []
        self.tpl_inserted = []
        self.tpl_export = []
        self.current_load = 1
        self.meta = {
            'author': 'Tristan Granier',
            'type': 'website',
            'description': 'Parse integrated link from selected website.'
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

    def parse_domain(self, url):
        if "://" in url:
            url = url.split('://')[1]
        if "." in url:
            url = url.split('.', 1)[0]
        return url

    def extract_url(self, url):
        next_page = ""
        nexts = 0
        try:
            req = requests.get(url)
            nexts = 1
        except:
            self.tpl_export.append({
                'URL': "Unknown link" + str(url)
            })
            self.export.append(self.tpl_export)
        if nexts == 1:
            if url[-1:] == "/":
                url = url[:-1]
            if url not in self.already and self.parse_domain(self.get_options('website')) in url:
                html = req.content
                soup = BeautifulSoup(html, "html.parser")
                link_count = len(soup.findAll('a'))
                self.already.append(url)
                print Fore.YELLOW + "* Load : " + str(url) + " with " + str(link_count) + " total link" + Style.RESET_ALL
                for a in soup.findAll('a'):
                    try:
                        if a['href'] != "":
                            total_link = a['href']
                            if total_link[:1] == "?":
                                total_link = url + "/" + str(total_link)
                            if total_link[:1] == "/":
                                total_link = url + total_link
                            elif total_link[:2] == "//":
                                total_link = total_link.replace('//',url + "/")
                            elif total_link[:1] == "#":
                                total_link = url + "/" + total_link
                            elif "://" not in total_link[:8]:
                                total_link = url + "/" + total_link
                            if "mailto:" not in total_link:
                                if total_link not in self.tpl_inserted and a['href'] not in self.linked:
                                    if total_link != "":
                                        self.tpl_export.append({
                                            'URL': total_link,
                                            '_id': self.generate_unique_id()
                                        })
                                    self.tpl_inserted.append(total_link)
                                    self.linked.append(a['href'])
                    except:
                        err = 1
                if self.current_load <= int(self.get_options('page_limit')):
                    if len(self.tpl_export) > 0:
                        next_page = self.tpl_export[self.current_load]
                        if next_page != "":
                            self.current_load += 1
                            self.extract_url(next_page['URL'])
                        else:
                            self.export.append(self.tpl_export)
                self.export.append(self.tpl_export)
                return True

    def main(self):
        tpl_export = []
        nexts = 0
        website = self.get_options('website')
        if "http//" in website:
            website = website.replace('http//', 'http://')
        try:
            req = requests.get(website)
            nexts = 1
        except:
            tpl_export.append({
                'information': "This link is not stable.",
                '_id': self.generate_unique_id()
            })
            self.export.append(tpl_export)
        if nexts == 1:
            self.extract_url(website)

