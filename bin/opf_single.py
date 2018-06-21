#!/usr/bin/env  python

import sys
from colorama import Fore, Style
import os
import glob
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
            'description': 'Run module single module'
        }
        self.directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0]
        if error == 1:
            self.directory = os.path.expanduser('~') + "/.operative_framework"
        self.module_class = ""
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
            self.print_help()
        options = sys.argv[1]
        if options == "--list":
            self.module_lists()
        elif options == "--use" and len(sys.argv) == 3:
            if "/" not in sys.argv[2]:
                print "please use correct format ex: --use website/whois_domain"
                return False
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
                self.shell_help()
                while action == 0:
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
                                argument_v = cmd[1].split('=')
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
    except:
        print "\nbye..."