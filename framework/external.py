#!/usr/bin/env  python

import sys
import os
import datetime
import logging
from engine import session
from optparse import OptionParser
from pymongo import MongoClient
import config


def write_log(log_header="", log_text="", element_name=""):
    if os.path.isfile('engine/logs/external.log'):
        with open('engine/logs/external.log', "a") as log_file:
            if log_header == "":
                log_header = "["+str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M'))+"]"
            if element_name != "":
                element_name = "EXECUTE " + str(element_name)
            log_file.write(log_text + " " + log_header + "  " + element_name + "\n")
            log_file.close()
    return True
    #logging.basicConfig(filename='engine/logs/external.log', level=logging.DEBUG)


def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    print directory
    logging.basicConfig(filename=directory + '/engine/logs/external.log', level=logging.DEBUG)
    if len(sys.argv) < 2:
        sys.exit("use -h for help.")
    parser = OptionParser(usage="usage: %prog [options] -s session_name", version="%prog 1.0")
    parser.add_option("-s", "--session", dest="session_name", help="open a session")
    parser.add_option("-i", "--id", dest="session_id", help="session_id")
    (options, args) = parser.parse_args()

    if options.session_name and options.session_id:
        client = MongoClient('mongodb://'+str(config.MONGODB_USER)+':'+str(config.MONGODB_PASS)+'@'+str(config.MONGODB_HOST)+':'+str(config.MONGODB_PORT)+'/tracking?authSource=operative_framework')
        database = client.operative_framework
        sess = session.Sess(options.session_name)
        if sess.exist():
            try:
                collection = database.running_modules
                if collection.find({"task_id": options.session_id}).count() > 0:
                    module_class = sess.load_session()
                    try:
                        module_class.main()
                        if len(module_class.export) > 0:
                            if len(module_class.export[0]) > 0:
                                group_by = ""
                                if "group_by" in module_class.meta:
                                    group_by = module_class.meta['group_by']
                                collection.update({"task_id": options.session_id}, {
                                    '$set': {"results": module_class.export, 'status': "executed", "error_msg": "", "group_by": group_by}})
                            else:
                                collection.update({"task_id": options.session_id}, {
                                    '$set': {"results": module_class.export, 'status': "empty", "error_msg": ""}})
                        else:
                            collection.update({"task_id": options.session_id}, {
                                '$set': {"results": module_class.export, 'status': "empty", "error_msg": ""}})
                    except Exception as e:
                        collection.update({"task_id": options.session_id},
                                          {'$set': {"results": module_class.export, 'status': "error", 'error_msg': str(e)}})
                    sess.delete_session()
                else:
                    sys.exit("[ERROR] Session / id not found.")
            except Exception as e:
                write_log(log_text=str(e), element_name="external.py")
        else:
            sys.exit("[ERROR] Session / id not found.")


if "__main__" == __name__:
    main()
