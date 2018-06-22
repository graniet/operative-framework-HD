#!/usr/bin/env  python

import sys
import os
import glob
from colorama import Fore, Style
error = 0
try:
    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0])
    from framework import config
    from framework.external_tool import integrated
    from bin import opf_client, opf_server
except:
    error = 1
try:
    sys.path.insert(0, os.path.expanduser('~') + "/.operative_framework/")
    from framework import config
    from framework.external_tool import integrated
except:
    error = 2

class OperativeBinary(object):

    def __init__(self):
        self.meta = {
            'author': 'Tristan Granier',
            'description': 'Importer database management'
        }
        self.directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0]
        if error == 1:
            self.directory = os.path.expanduser('~') + "/.operative_framework"
        self.module_class = ""

    def print_help(self):
        print "Usage: " + sys.argv[0] + " [options]"
        print "options listing:"
        print "--use <Importer> " + Fore.YELLOW + "use specific importer." + Style.RESET_ALL
        print "--list " + Fore.YELLOW + "listing of importers name." + Style.RESET_ALL
        return False

    def importers_list(self):
        if os.path.exists(self.directory + "/framework/importers/"):
            modules = glob.glob(self.directory + "/framework/importers/*.py")
            for m in modules:
                m_path = m
                m_shortcut = m_path.replace('/', '.').split('.py')[0]
                m_shortcut = m_shortcut.split('.framework')[1]
                m_shortcut = "framework" + m_shortcut
                m_name = m_shortcut.split('.')[-1]
                if m_name != "__init__" and m_name != "sample_module":
                    try:
                        mod = __import__(m_shortcut, fromlist=['OpfImporter'])
                        module_class = mod.OpfImporter()
                        if hasattr(module_class, "meta"):
                            print "- " + m_name + " :   " + Fore.YELLOW + module_class.meta['description'] + Style.RESET_ALL
                    except Exception as e:
                        module_error = 1

    def print_module_help(self):
        print "help : " + Fore.YELLOW + "print this bullet" + Style.RESET_ALL
        print "run :    " + Fore.YELLOW + "run importer" + Style.RESET_ALL
        print "argv :   " + Fore.YELLOW + "view module arguments" + Style.RESET_ALL
        print "set argument=value :  " + Fore.YELLOW + "set argument from module" + Style.RESET_ALL

    def view_required(self):
        module = self.module_class
        if len(module.arguments) > 0:
            for element in module.arguments:
                if element['required'] == "yes":
                    print "- " + element['name'] + " (" + Fore.RED + "required" + Style.RESET_ALL + ") : '" + element['value']+"'"
                elif element['required'] == "no":
                    print "- " + element['name'] + " : '" + element[
                        'value']+"'"

    def set_argument(self, argument, value):
        module = self.module_class
        if len(module.arguments) > 0:
            for element in module.arguments:
                if element['name'].lower() == argument.lower():
                    element['value'] = value
        self.module_class = module
        return True

    def execute(self):
        module = self.module_class
        module.run()
        self.module_class = module
        return True

    def run(self):
        if len(sys.argv) < 2:
            self.print_help()
        options = sys.argv[1]
        if options == "--list":
            self.importers_list()
        elif options == "--use" and len(sys.argv) == 3:
            module_base = sys.argv[2]
            if os.path.isfile(self.directory + "/framework/importers/" + module_base + ".py"):
                try:
                    mod = __import__("framework.importers." + module_base, fromlist=['OpfImporter'])
                    module_class = mod.OpfImporter()
                except:
                    print "Can't load module, please retry."
                    return False
                action = 0
                self.module_class = module_class
                self.print_module_help()
                while action == 0:
                    user_put = raw_input("opf/importer ("+Fore.YELLOW+str(module_base)+Style.RESET_ALL+") > ")
                    user_put = user_put.strip()
                    if user_put == "help":
                        self.print_module_help()
                    elif user_put == "argv":
                        self.view_required()
                    elif " " in user_put:
                        cmd = user_put.split(' ')
                        if cmd[0].strip() == "set":
                            if len(cmd) == 2 and "=" in cmd[1]:
                                argument_v = cmd[1].split('=')
                                self.set_argument(argument_v[0], argument_v[1])
                                print Fore.GREEN + "=> " + Style.RESET_ALL + "command executed."
                            else:
                                print "format wrong please use : set argument=value"
                    elif user_put == "run":
                        self.execute()
                        if module_class.error_message != "":
                            print Fore.RED + "=> " + Style.RESET_ALL + str(module_class.error_message)
                        else:
                            print Fore.GREEN + "=> " + Style.RESET_ALL + "command executed."


if __name__ == "__main__":
    try:
        OperativeBinary().run()
    except Exception as (e):
        print "\nbye..."
        print str(e)