#!/usr/bin/env  python

import sys
from colorama import Fore, Style
import os
import glob
from optparse import OptionParser
import readline
import json

error = 0
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

class OperativeBinary(object):

    def __init__(self):
        self.meta = {
            'author': 'Tristan Granier',
            'description': 'Run single module'
        }
        self.directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0]
        if error == 1:
            self.directory = os.path.expanduser('~') + "/.operative_framework"
        self.module_class = ""
        self.export_json = False
        self.verbose = True
        self.json_dump = {}
        self.run()

    def module_lists(self):
        if os.path.exists(self.directory + "/framework/engine/modules/"):
            modules = glob.glob(self.directory + "/framework/engine/modules/*.py")
            for m in modules:
                m_path = m
                m_path = m_path.replace('core', 'engine')
                m_shortcut = m_path.replace('/', '.').split('.py')[0]
                m_shortcut = m_shortcut.replace('core', 'framework.engine')
                m_shortcut = m_shortcut.split('.framework')[1]
                m_shortcut = "framework" + m_shortcut
                m_name = m_shortcut.split('.')[-1]
                if m_name != "__init__" and m_name != "sample_module":
                    try:
                        mod = __import__(m_shortcut, fromlist=['module_element'])
                        module_class = mod.module_element()
                        if hasattr(module_class, "meta"):
                            print "- " + module_class.meta['type'] + "/" + m_name + " :   " + Fore.YELLOW + module_class.meta['description'] + Style.RESET_ALL
                    except Exception as e:
                        module_error = 1

    def print_help(self):
        print "Usage: " + sys.argv[0] + " [options]"
        print "options listing:"
        print "--use <ModuleName> " + Fore.YELLOW + "use specific module." + Style.RESET_ALL
        print "--list " + Fore.YELLOW + "listing of module name." + Style.RESET_ALL
        return False

    def view_required(self):
        module = self.module_class
        if len(module.require) > 0:
            for element in module.require:
                if element['required'] == "yes":
                    print "- " + element['name'] + " (" + Fore.RED + "required" + Style.RESET_ALL + ") : " + element['value']
                elif element['required'] == "no":
                    print "- " + element['name'] + " : " + element[
                        'value']

    def shell_help(self):
        print "help : " + Fore.YELLOW + "print this bullet" + Style.RESET_ALL
        print "run :    " + Fore.YELLOW + "run argument" + Style.RESET_ALL
        print "export : " + Fore.YELLOW + "view exported result" + Style.RESET_ALL
        print "argv :   " + Fore.YELLOW + "view module arguments" + Style.RESET_ALL
        print "set argument=value :  " + Fore.YELLOW + "set argument from module" + Style.RESET_ALL


    def set_argument(self, argument, value):
        module = self.module_class
        if len(module.require) > 0:
            for element in module.require:
                if element['name'].lower() == argument.lower():
                    element['value'] = value
        self.module_class = module
        return True

    def execute(self):
        module = self.module_class
        module.main()
        self.module_class = module
        return True


    def export_raw(self):
        module = self.module_class
        if len(module.export) > 0:
            results = module.export
            for element in results:
                if hasattr(element, "__len__"):
                    for result in element:
                        if "_id" in result:
                            print Fore.GREEN + "_id:" + result['_id']+ Style.RESET_ALL
                        for key, value in result.iteritems():
                            if key != "_id":
                                print "| " + str(key) + " : " + str(value)
                else:
                    print "no("
                    print element
        else:
            print Fore.YELLOW + "=> "+Style.RESET_ALL+"Result as empty."


    def run(self):
        if len(sys.argv) < 2:
            print "use -h for help."
            sys.exit()
        parser = OptionParser(usage="usage: %prog [options] -u enterprise/linkedin_search -a enterprise=github -r", version="%prog 1.0")
        parser.add_option("-l", "--list", action="store_false", dest="module_list", help="listing of module name.")
        parser.add_option("-a", "--args", dest="module_argument", help="add arguments to module")
        parser.add_option("-r", "--run", action="store_false", dest="module_run", help="run module")
        parser.add_option("-u", "--use", dest="module_name", metavar="module_name", help="use specific module")
        parser.add_option("-j", "--json", action="store_false", dest="export_json", help="print result to json")
        (options, args) = parser.parse_args()
        if options.module_list is not None:
            self.module_lists()
        elif options.module_name is not None:
            if "/" not in sys.argv[2]:
                print "please use correct format ex: --use website/whois_domain"
                sys.exit()
            module_base = sys.argv[2]
            module_name = sys.argv[2].split('/')[1]
            if os.path.isfile(self.directory + "/framework/engine/modules/" + module_name + ".py"):
                try:
                    mod = __import__("framework.engine.modules." + module_name, fromlist=['module_element'])
                    module_class = mod.module_element()
                except:
                    print "Can't load module, please retry."
                    return False
                action = 0
                self.module_class = module_class
                if options.module_argument is not None:
                    if ";" in options.module_argument:
                        arguments_list = options.module_argument.split(';')
                        for argument in arguments_list:
                            if "=" in argument:
                                argument_v = argument.split('=', 1)
                                self.set_argument(argument_v[0], argument_v[1])
                            else:
                                print "format wrong please use : set argument=value"
                                sys.exit()
                    else:
                        if "=" in options.module_argument:
                            argument_v = options.module_argument.split('=', 1)
                            self.set_argument(argument_v[0], argument_v[1])
                        else:
                            print "format wrong please use : set argument=value"
                            sys.exit()
                    if options.module_run is not None:
                        self.execute()
                        if options.export_json is None:
                            self.export_raw()
                        else:
                            self.json_dump['informations'] = self.module_class.meta
                            if hasattr(self.module_class.export, "__len__"):
                                self.json_dump['results'] = self.module_class.export[0]
                            else:
                                self.json_dump['results'] = self.module_class.export
                            print json.dumps(self.json_dump)
                        return True
                self.shell_help()
                while action == 0 and options.module_run is None:
                    user_put = raw_input('$ operative ('+Fore.YELLOW+module_base+ Style.RESET_ALL+') > ')
                    user_put = user_put.strip()
                    if user_put == "help":
                        self.shell_help()
                    elif user_put == "argv":
                        self.view_required()
                    elif " " in user_put:
                        cmd = user_put.split(' ')
                        if cmd[0].strip() == "set":
                            if len(cmd) == 2 and "=" in cmd[1]:
                                argument_v = cmd[1].split('=', 1)
                                self.set_argument(argument_v[0], argument_v[1])
                                print Fore.GREEN + "=> " + Style.RESET_ALL + "command executed."
                            else:
                                print "format wrong please use : set argument=value"
                    elif user_put == "run":
                        self.execute()
                        print Fore.GREEN + "=> " + Style.RESET_ALL + "command executed."
                    elif user_put == "export":
                        self.export_raw()
            else:
                print "please select correct module, for module list please use '"+sys.argv[0]+" --list'"
                return False
        else:
            self.print_help()

if __name__ == "__main__":
    try:
        OperativeBinary()
    except KeyboardInterrupt:
        print "\nbye..."