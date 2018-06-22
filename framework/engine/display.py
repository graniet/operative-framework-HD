#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import os
try:
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0])
    from framework import config
except:
    error = 1
try:
    sys.path.insert(0, os.path.expanduser('~') + "/.operative_framework/")
    from framework import config
except:
    error = 2


def work(random_id, module_class, database):
    module_class.main()
    collection = database.running_modules
    collection.update({"task_id": random_id}, {'$set': {"results": module_class.export}})