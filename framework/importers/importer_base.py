#!/usr/bin/env  python


import string
import random
import datetime
from pymongo import MongoClient
from framework import config


class OpfBaseImporter(object):

    def __init__(self):
        self.client = MongoClient('mongodb://' + str(config.MONGODB_USER) + ':' + str(config.MONGODB_PASS) + '@' + str(
            config.MONGODB_HOST) + ':' + str(config.MONGODB_PORT) + '/tracking?authSource=operative_framework')
        self.database = self.client.operative_framework

    def get_argument(self, name, arguments):
        for argument in arguments:
            if argument['name'] == name:
                return argument['value']
        return False

    def set_error(self, string):
        self.error_message = string

    def check_argument(self, arguments):
        for argument in arguments:
            if argument['required'] == 'yes' and argument['value'] == '':
                return False
        return True

    def random_breach(self, size=6, chars=string.ascii_uppercase + string.digits):
        collection = self.database.public_breach
        start = 0
        breach_id = ""
        while start == 0:
            breach_id = ''.join(random.choice(chars) for _ in range(size))
            if collection.find({'breach_id': breach_id}).count() < 1:
                start = 1
        return breach_id

    def random_breach_content(self, size=40, chars=string.ascii_uppercase + string.digits):
        collection = self.database.public_breach_content
        start = 0
        breach_content_id = ""
        while start == 0:
            breach_content_id = ''.join(random.choice(chars) for _ in range(size))
            if collection.find({'breach_content_id': breach_content_id}).count() < 1:
                start = 1
        return breach_content_id

    def get_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')