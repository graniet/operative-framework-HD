#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import glob
import os
import string
import sys
import random
import hashlib
import subprocess
import datetime
from pymongo import MongoClient, DESCENDING, errors
from engine import config, display, session
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString


class Engine(object):

    def __init__(self, hostname, port):
        self.client = MongoClient('mongodb://'+str(config.MONGODB_USER)+':'+str(config.MONGODB_PASS)+'@'+str(config.MONGODB_HOST)+':'+str(config.MONGODB_PORT)+'/tracking?authSource=operative_framework')
        if not self.random_query():
            sys.exit('Please configure/start correctly MongoDB database with --auth.')
        self.database = self.client.operative_framework
        self.default_module_tpl = {
            "_id": False,
            "module_name": True,
            "module_import": True,
            "module_path": True,
            "module_description": True
        }
        self.directory = os.path.dirname(os.path.realpath(__file__)).rsplit('/', 1)[0]
        self.three_template = []
        self.user_right = [
            'Administrator',
            'Contributor',
            'Viewer'
        ]
        self.write_right = [
            'Administrator',
            'Contributor'
        ]

    def select_module(self, by="module_name", search="", limit=1):
        collection = self.database.modules
        if limit == "*":
            return {
                "count": collection.find({}, self.default_module_tpl).count(),
                "modules": list(collection.find({}, self.default_module_tpl))
            }
        return list(collection.find({by: search}).limit(limit))

    def random_query(self):
        try:
            self.client.server_info()
        except errors.ServerSelectionTimeoutError as err:
            return False
        return True

    def write_log(self, log_header="", log_text="", element_name=""):
        if os.path.isfile(self.directory + '/engine/logs/webserver.log'):
            with open(self.directory + '/engine/logs/webserver.log', "a") as log_file:
                if log_header == "":
                    log_header = "[" + str(datetime.datetime.today().strftime('%Y-%m-%d %H:%M')) + "]"
                if element_name != "":
                    element_name = "EXECUTE " + str(element_name)
                log_file.write(log_text + " " + log_header + "  " + element_name + "\n")
                log_file.close()
        return True

    def insert_module(self, module):
        collection = self.database.modules
        if collection.find({"name": module['name']}).count() < 1:
            collection.insert(module)
            return True
        return False

    def insert_module_manual(self, template):
        collection = self.database.modules
        if collection.find(template).count() < 1:
            collection.insert(template)
            return True
        return False

    def load_modules(self):
        errors_modules = []
        if os.path.exists("engine/modules/"):
            modules = glob.glob("engine/modules/*.py")
            for m in modules:
                m_path = m
                m_path = m_path.replace('core', 'engine')
                m_shortcut = m_path.replace('/', '.').split('.py')[0]
                m_shortcut = m_shortcut.replace('core', 'engine')
                m_name = m_shortcut.split('.')[-1]
                m_source = open(m).read()
                if m_name != "__init__" and m_name != "sample_module":
                    try:
                        mod = __import__(m_shortcut, fromlist=['module_element'])
                        module_class = mod.module_element()
                        if hasattr(module_class, "meta"):
                            result_output = "rows"
                            export_primary = ""
                            export_category = ""
                            if "result" in module_class.meta:
                                result_output = module_class.meta['result']
                            if "export_primary" in module_class.meta:
                                export_primary = module_class.meta['export_primary']
                            if "export_category" in module_class.meta:
                                export_category = module_class.meta['export_category']
                            m_template = {
                                "module_name": m_name,
                                "module_import": m_shortcut,
                                "module_path": m_path,
                                "module_type": module_class.meta['type'],
                                "module_author": module_class.meta['author'],
                                "module_description": module_class.meta['description'],
                                "module_result_output": result_output,
                                'module_argument': module_class.require,
                                "module_export_primary": export_primary,
                                "module_export_category": export_category,
                            }
                            print "+ " + str(m_shortcut)
                            self.insert_module_manual(m_template)
                    except Exception as e:
                        print str(e)
                        errors_modules.append(m_shortcut)
        return True

    def random_tasks(self, size=6, chars=string.ascii_uppercase + string.digits, auth_token="", module_name="", project_id="alone", subject="", module_output="alone", module_export_primary=""):
        if auth_token != "":
            collection = self.database.users
            current_user = collection.find({'auth_token': auth_token})
            if current_user.count() < 1:
                return False
            current_user = list(current_user)
            app_id = current_user[0]['app_id']
            current_user = current_user[0]['username']
            collection = self.database.running_modules
            start = 0
            task = ""
            while start == 0:
                task = ''.join(random.choice(chars) for _ in range(size))
                if collection.find({'task_id': task, 'username': current_user}).count() < 1:
                    collection.insert({'task_id': task, 'username': current_user, 'results': "", 'status': 'pending', 'module_name': module_name, 'project_id': project_id, 'app_id': app_id, 'project_subject': subject, 'created_at': self.get_date(), 'error_msg': "", 'module_output': module_output, 'module_export_primary': module_export_primary})
                    start = 1
            return task
        return False

    def random_token(self, size=6, chars=string.ascii_uppercase + string.digits):
        collection = self.database.users
        start = 0
        auth_token = ""
        while start == 0:
            auth_token = ''.join(random.choice(chars) for _ in range(size))
            if collection.find({'auth_token': auth_token}).count() < 1:
                start = 1
        return auth_token

    def random_letter(self, size=6, chars=string.ascii_uppercase + string.digits, prefix=""):
        collection = self.database.users
        start = 0
        auth_token = ""
        while start == 0:
            auth_token = prefix + ''.join(random.choice(chars) for _ in range(size))
            if collection.find({'app_id': auth_token}).count() < 1:
                start = 1
        return auth_token

    def random_project(self, size=6, chars=string.ascii_uppercase + string.digits, prefix=""):
        collection = self.database.projects
        start = 0
        auth_token = ""
        while start == 0:
            auth_token = prefix + ''.join(random.choice(chars) for _ in range(size))
            if collection.find({'project_id': auth_token}).count() < 1:
                start = 1
        return auth_token

    def random_element(self, size=6, chars=string.ascii_uppercase + string.digits, prefix=""):
        collection = self.database.projects_elements
        start = 0
        auth_token = ""
        while start == 0:
            auth_token = prefix + ''.join(random.choice(chars) for _ in range(size))
            if collection.find({'element_id': auth_token}).count() < 1:
                start = 1
        return auth_token

    def module_information(self, module_import):
        collection = self.database.modules
        m_path = module_import.replace('.', '/')
        m_exist = False
        if os.path.exists(m_path + ".py") and collection.find({}, {"module_import": module_import}).count() > 0:
            mod = __import__(module_import, fromlist=['module_element'])
            module_class = mod.module_element()
            m_exist = True
            m_information = list(collection.find({"module_import": module_import}, self.default_module_tpl))
            m_arguments = module_class.require

            return {
                "status": "success",
                "module_found": m_exist,
                "module_import": module_import,
                "module_informations": m_information,
                "module_arguments": m_arguments,
            }

        else:
            return {
                "status" : "forbidden",
                "module_import": module_import,
                "module_found": m_exist
            }

    def module_treading(self, random_id, module_class):
        module_class.main()
        collection = self.database.running_modules
        collection.update({"task_id": random_id}, {'$set': {"results": module_class.export}})

    def task_view(self, task_id, auth_token, app_id):
        collection_user = self.database.users
        if collection_user.find({'auth_token': auth_token, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access",
                'status': "forbidden"
            }

        collection = self.database.running_modules
        result = collection.find({"task_id": task_id, 'app_id': app_id}, {"_id": False, "task_id": True, "results": True, "status": True})
        if result.count() > 0:
            return list(result)
        else:
            return {"msg": "Task not found."}

    def execute_module(self, auth_token, module_import, post_data):
        collection = self.database.modules
        argument_list = []
        exist = collection.find({"module_import": module_import}).count()
        if not exist:
            return {"msg": "Module not found."}
        mod = __import__(module_import, fromlist=['module_element'])
        module_class = mod.module_element()
        arguments = module_class.require
        argument_error = False
        argument_required = 0
        for argument in arguments:
            argument_list.append(argument['name'])
            if argument['required'] == "yes":
                argument_required = argument_required + 1
                if argument['name'] not in post_data:
                    argument_error = True
                else:
                    argument['value'] = post_data[argument['name']]
            else:
                if argument['name'] in post_data:
                    argument['value'] = post_data[argument['name']]
        for argv in post_data:
            if argv not in argument_list:
                argument_error = True
        if len(post_data) >= argument_required and not argument_error:
            random_id = self.random_tasks(8, auth_token=auth_token, module_name=module_import)
            if random_id == False:
                return {'status': 'forbidden', 'msg': 'users not found.'}
            module_class.database_id = random_id
            self.session = session.Sess(random_id)
            self.session.generate(module_class)
            try:
                subprocess.Popen(['/usr/bin/python', self.directory + '/external.py', '-s', random_id, '-i', random_id],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                return {
                    "status": "forbidden",
                    "msg": "not found (err: 9nDhF)."
                }
            return {
                "status": "success",
                "task_id": random_id,
                "module_import": module_import
            }
        return {
            "status": "forbidden",
            "msg": "Configuration not allowed."
        }

    def execute_project_module(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "module_import" not in post_data or "module_argument" not in post_data \
                or "project_id" not in post_data or "project_subject" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }
        module_import = post_data['module_import']
        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        filled_argument = post_data['module_argument']
        project_subject = post_data['project_subject']

        collection = self.database.modules
        argument_list = []
        exist = collection.find({"module_import": module_import}).count()
        if not exist:
            return {
                'status': "forbidden",
                'msg': "Module not found."
            }
        mod = __import__(module_import, fromlist=['module_element'])
        module_class = mod.module_element()
        module_output = "rows"
        module_export_primary = ""
        if hasattr(module_class, "meta"):
            if "result" in module_class.meta:
                module_output = module_class.meta['result']
            if "export_primary" in module_class.meta:
                module_export_primary = module_class.meta['export_primary']
        arguments = module_class.require
        argument_error = False
        argument_required = 0
        for argument in arguments:
            argument_list.append(argument['name'])
            if argument['required'] == "yes":
                argument_required = argument_required + 1
                if argument['name'] not in filled_argument:
                    argument_error = True
                else:
                    argument['value'] = filled_argument[argument['name']]
            else:
                if argument['name'] in filled_argument:
                    argument['value'] = filled_argument[argument['name']]
        for argv in filled_argument:
            if argv not in argument_list:
                argument_error = True
        if len(filled_argument) >= argument_required and not argument_error:
            random_id = self.random_tasks(8, auth_token=auth_token, module_name=module_import, project_id=project_id, subject=project_subject, module_output=module_output, module_export_primary=module_export_primary)
            if random_id == False:
                return {
                    'status': 'forbidden',
                    'msg': 'users not found.'
                }
            module_class.database_id = random_id
            select_task = self.database.running_modules.find({'task_id': random_id}, {'_id': False})
            self.session = session.Sess(random_id)
            self.session.generate(module_class)
            try:
                subprocess.Popen(['sudo', '/usr/bin/python', self.directory + '/external.py', '-s', random_id, '-i', random_id],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                return {
                    "status": "forbidden",
                    "msg": "not found (err: external_executor_module)."
                }
            return {
                "status": "success",
                "task_id": random_id,
                "task": list(select_task)[0],
                "module_import": module_import
            }
        return {
            "status": "forbidden",
            "msg": "Configuration not allowed."
        }

    def login_user(self, post_data):
        if "u_name" not in post_data or "u_password" not in post_data:
            return {
                'status': 'forbidden',
                'msg': "Format not available please use (u_name=username, u_password=password)"
            }
        collection = self.database.users
        u_name = post_data['u_name']
        u_password = hashlib.sha512(post_data['u_password'].encode()).hexdigest()
        if collection.find({'username': u_name, 'password': u_password}).count() < 1:
            return {
                'status': 'forbidden',
                'msg': "username/password combination are incorrect."
            }
        auth_token = self.random_token(12)
        collection.update({'username': u_name, 'password': u_password}, {'$set': {'auth_token': auth_token}})
        result = collection.find({'username': u_name, 'password': u_password}, {'_id': False, 'password': False})
        for element in result:
            return {
                'status': 'success',
                'auth_token': str(element['auth_token']),
                'app_id': str(element['app_id']),
                'user_name': element['username'],
                'msg': "success login-in"
            }

    def register_user(self, post_data):
        if "u_name" not in post_data or "u_password" not in post_data:
            return {'msg': "Format not available please use (u_name=username, u_password=password)"}
        collection = self.database.users
        u_name = post_data['u_name']
        u_password = hashlib.sha512(post_data['u_password'].encode()).hexdigest()
        if collection.find({'username': u_name}).count() > 0:
            return {'msg': "username already found."}
        auth_token = self.random_tasks(12)
        app_id = self.random_letter(size=8, prefix="APP_")
        collection.insert({'username': u_name, 'password': u_password, 'auth_token': auth_token, 'app_id': app_id, 'user_right': "Administrator"})
        return {
            'username': u_name,
            'app_id': app_id,
            'status': "success",
            'auth_token': auth_token
        }

    def register_user_team(self, post_data):
        collection = self.database.users
        if "u_username" not in post_data or "u_password" not in post_data \
            or "u_repassword" not in post_data or "u_app_id" not in post_data \
                or "u_auth_token" not in post_data or 'u_right' not in post_data:
            return {
                'msg': "Please send all asked field.",
                'status': "forbidden"
            }

        username = post_data['u_username']
        app_id = post_data['u_app_id']
        auth_token = post_data['u_auth_token']
        u_password = hashlib.sha512(post_data['u_password'].encode()).hexdigest()
        u_repassword = hashlib.sha512(post_data['u_repassword'].encode()).hexdigest()
        u_right = post_data['u_right']
        check_status = collection.find({'app_id': app_id, 'auth_token': auth_token, 'user_right': 'Administrator'})
        if check_status.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        check_user = collection.find({'app_id': app_id, 'username': username})
        if check_user.count() > 0:
            return {
                'msg': "Team member already found.",
                'status': "forbidden"
            }

        if u_password != u_repassword:
            return {
                'msg': "Password and Repassword not egual.",
                'status': "forbidden"
            }

        if u_right not in self.user_right:
            return {
                'msg': "Please setup correct user right.",
                'status': 'forbidden'
            }

        collection.insert({'username': username, 'app_id': app_id, 'auth_token': "",
                                    'password': u_password, 'user_right': u_right})
        return {
            'msg': "Team members as been added!",
            'status': "success"
        }

    def remove_user_team(self, post_data):
        collection = self.database.users
        if "u_username" not in post_data or "u_auth_token" not in post_data \
            or "u_app_id" not in post_data:
            return {
                'msg': "Please setup all required field.",
                'status': "forbidden"
            }

        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        username = post_data['u_username']
        check_user = collection.find({'auth_token': auth_token, 'app_id': app_id, "user_right": "Administrator"})
        if check_user.count() < 1:
            return {
                'msg': "You don't have access right",
                'status': "forbidden"
            }

        check_team_member = collection.find({'app_id': app_id, 'username': username})
        if check_team_member.count() < 1:
            return {
                'msg': "Team member not found.",
                'status': "forbidden"
            }

        collection.remove({'app_id': app_id, 'username': username})
        return {
            'msg': "Member successfully deleted.",
            'status': "success"
        }

    def get_date(self):
        return datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    def check_login(self, auth_token, app_id):
        collection = self.database.users
        if collection.find({'auth_token': auth_token, 'app_id': app_id}).count() > 0:
            return {
                'action': 'check_auth_token',
                'executed': datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
                'status': 'success'
            }
        return {
            'action': 'check_auth_token',
            'executed': datetime.datetime.today().strftime('%Y-%m-%d %H:%M'),
            'status': 'forbidden'
        }

    def user_information(self, auth_token):
        collection = self.database.users
        return {
            'msg': "ok"
        }

    def task_all(self, auth_token):
        collection = self.database.users
        check_user = collection.find({'auth_token': auth_token})
        if check_user.count() < 1:
            return {
                'status': 'forbidden',
                'msg': 'user not found.',
            }
        check_user = list(check_user)
        current_username = check_user[0]['username']
        current_app_id = check_user[0]['app_id']
        collection = self.database.running_modules
        tasks = collection.find({'app_id': current_app_id}, {'_id': False, 'results': False,})
        if tasks.count() < 1:
            return {
                'status': 'success',
                'tasks': []
            }
        return {
            'status': 'success',
            'tasks': list(tasks)
        }

    def task_view_unique(self, task_id, auth_token):
        collection = self.database.running_modules
        user_information = self.database.users.find({'auth_token': auth_token}, {"_id": False})
        if user_information.count() < 1:
            return {
                'status': 'forbidden',
                'msg': "user not found."
            }
        user_information = list(user_information)[0]
        result = collection.find({'username': user_information['username'], 'task_id': task_id}, {"_id": False})
        if result.count() < 1:
            return {
                'status': 'forbidden',
                'msg': 'this task not found'
            }
        return {
            'status': 'success',
            'result': list(result)[0]
        }

    def get_teams(self, auth_token, app_id):
        collection = self.database.users
        find = collection.find({"auth_token": auth_token, "app_id": app_id})
        if find.count() < 1:
            return {
                "msg": "team not found.",
                "status": "forbidden"
            }
        teams = collection.find({"app_id": app_id}, {"_id": False, "password": False, "auth_token": False})
        return {"status": "success", "teams": list(teams)}

    def create_project(self, post_data):
        if "u_auth_token" not in post_data \
            or "u_app_id" not in post_data \
                or "project_name" not in post_data:
            return {
                'msg': "Please complete required field",
                'status': "forbidden"
            }

        collection_user = self.database.users
        app_id = post_data['u_app_id']
        auth_token = post_data['u_auth_token']
        user_result = collection_user.find({'app_id': app_id, 'auth_token': auth_token})
        user_right = ""
        user_name  = ""
        project_name = post_data['project_name']
        if user_result.count() < 1:
            return {
                'msg': "You don't have access.",
                'status': "forbidden"
            }

        for element in user_result:
            user_name  = element['username']
            user_right = element['user_right']

        if user_right not in self.write_right:
            return {
                'msg': "You don't have a write access",
                'status': "forbidden"
            }

        collection_project = self.database.projects
        project_id = self.random_project(size=12, prefix="project_" + app_id.split('APP_')[1])

        if project_name == "":
            return {
                'msg': "Please complete al required field",
                'status': "forbidden"
            }

        check_exist_project = collection_project.find({'app_id': app_id, 'project_name': project_name})
        if check_exist_project.count() > 0:
            return {
                'msg': "Project already exist.",
                'status': "forbidden"
            }
        collection_project.insert({
            'project_id': project_id,
            'app_id': app_id,
            'project_name': project_name,
            'created_by': user_name,
            'created_at': self.get_date()
        })
        return {
            'msg': "Project successfully created.",
            'status': "success"
        }

    def list_projects(self, auth_token, app_id):
        collection_user = self.database.users
        collection_project = self.database.projects

        if collection_user.find({'auth_token': auth_token, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access.",
                'status': "forbidden"
            }

        project_list = collection_project.find({'app_id': app_id}, {'_id': False})
        if project_list.count() < 1:
            return {
                'msg': "project returned.",
                'status': "success",
                'projects': []
            }
        return {
            'msg': "project returned.",
            'status': "success",
            'projects': list(project_list)
        }

    def view_project(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']

        if auth_token == "" or app_id == "" or project_id == "":
            return {
                'msg': "Please complete required field.",
                'status': "forbidden"
            }

        collection_users = self.database.users
        check_user = collection_users.find({'auth_token': auth_token, 'app_id': app_id}, {"_id": False})
        if check_user.count() < 1:
            return {
                'msg': "You can't access here.",
                'status': "forbidden"
            }

        collection_project = self.database.projects
        check_project = collection_project.find({'project_id': project_id, 'app_id': app_id}, {"_id": False})
        if check_project.count() < 1:
            return {
                'msg': "Project not found.",
                'status': "forbidden"
            }

        collection_subject = self.database.projects_elements
        select_subjects = collection_subject.find({'project_id': project_id, 'app_id': app_id, 'element_type': "subject"}, {"_id": False})

        collection_tasks = self.database.running_modules
        select_tasks = collection_tasks.find({'project_id': project_id, 'app_id': app_id}, {"_id": False}).sort('created_at', DESCENDING)

        project_information = []
        for element in check_project:
            project_information = element

        return {
            "executed_at": self.get_date(),
            'status': "success",
            'tasks': list(select_tasks),
            'subjects': list(select_subjects),
            'projects': project_information
        }

    def find_linked_from_key(self, element_list, element):
        for key, subject in enumerate(element_list):
            if subject['name'] == element:
                return key
        return "error_string"

    def get_linked_from(self, element_list, already_checked, new_list, project_id):
        collection_subject = self.database.projects_elements
        checked = 0
        for key, subject in enumerate(element_list):
            found = 0
            if subject['linked_from'] != "" and subject['name'] not in already_checked:
                check_if_linked = collection_subject.find({'linked_from': subject['name'], 'project_id': project_id, 'element_type': 'subject'}, {'_id': False})
                if check_if_linked.count() < 1:
                    checked = 1
                    linked_from_key = self.find_linked_from_key(element_list, subject['linked_from'])
                    if linked_from_key != "error_string":
                        if subject['group_by'] == "":
                            if not self.find_name(element_list[linked_from_key]['children'], subject['name']):
                                element_list[linked_from_key]['children'].append(subject)
                        else:
                            if len(element_list[linked_from_key]['children']) > 0:
                                for el in element_list[linked_from_key]['children']:
                                    if el['name'] == subject['group_by']:
                                        if not self.find_name(el['children'], subject['name']):
                                            el['children'].append(subject)
                                            found = 1

                                if found == 0:
                                    if not self.find_name(element_list[linked_from_key]['children'],
                                                          subject['group_by']):
                                        element_list[linked_from_key]['children'].append(
                                            {
                                                'name': subject['group_by'],
                                                'children': []
                                            })
                                    for el in element_list[linked_from_key]['children']:
                                        if el['name'] == subject['group_by']:
                                            if subject not in el['children']:
                                                el['children'].append(subject)
                            else:
                                if not self.find_name(element_list[linked_from_key]['children'], subject['group_by']):
                                    element_list[linked_from_key]['children'].append(
                                        {
                                            'name': subject['group_by'],
                                            'children': []
                                        })
                                for el in element_list[linked_from_key]['children']:
                                    if el['name'] == subject['group_by']:
                                        if subject not in el['children']:
                                            el['children'].append(subject)
                        already_checked.append(subject['name'] + "_" + subject['element_id'])
                        del element_list[key]
                    else:
                        self.write_log(log_text="Can't find a parent '"+str(subject['linked_from'])+"' for '" + str(subject['name']) + "'", element_name="web.py")
                        del element_list[key]
                else:
                    can_put = True
                    for element in check_if_linked:
                        if element['element_text']['text'] + "_" + element['element_id'] not in already_checked:
                            linked_from_key = self.find_linked_from_key(element_list, subject['linked_from'])
                            if subject['group_by'] == "":
                                checked = 1
                                can_put = False
                            elif len(element_list[linked_from_key]['children']) > 0:
                                for el in element_list[linked_from_key]['children']:
                                    if el['name'] == subject['group_by']:
                                        if subject not in el['children']:
                                            el['children'].append(subject)
                                            found = 1
                                if found == 0:
                                    if not self.find_name(element_list[linked_from_key]['children'], subject['group_by']):
                                        element_list[linked_from_key]['children'].append(
                                            {
                                                'name': subject['group_by'],
                                                'children': []
                                            })
                                    for el in element_list[linked_from_key]['children']:
                                        if el['name'] == subject['group_by']:
                                            if not self.find_name(el['children'], subject['name']):
                                                el['children'].append(subject)
                            else:
                                if not self.find_name(element_list[linked_from_key]['children'], subject['group_by']):
                                    element_list[linked_from_key]['children'].append(
                                        {
                                            'name': subject['group_by'],
                                            'children': []
                                        })
                                for el in element_list[linked_from_key]['children']:
                                    if el['name'] == subject['group_by']:
                                        if not self.find_name(el['children'], subject['name']):
                                            el['children'].append(subject)
                            checked = 1
                            can_put = False
                    if can_put:
                        linked_from_key = self.find_linked_from_key(element_list, subject['linked_from'])
                        if linked_from_key != "error_string":
                            del element_list[key]
                            if subject['group_by'] == "":
                                element_list[linked_from_key]['children'].append(subject)
                            else:
                                if len(element_list[linked_from_key]['children']) > 0:
                                    for el in element_list[linked_from_key]['children']:
                                        if el['name'] == subject['group_by']:
                                            if not self.find_name(el['children'], subject['name']):
                                                el['children'].append(subject)
                                else:
                                    if not self.find_name(element_list[linked_from_key]['children'],
                                                          subject['group_by']):
                                        element_list[linked_from_key]['children'].append(
                                            {
                                                'name': subject['group_by'],
                                                'children': []
                                            })
                                    for el in element_list[linked_from_key]['children']:
                                        if el['name'] == subject['group_by']:
                                            if subject not in el['children']:
                                                el['children'].append(subject)

                            already_checked.append(subject['name'] + "_" + subject['element_id'])
        if checked == 1:
            new_list = element_list
            self.get_linked_from(element_list=element_list, already_checked=already_checked, new_list=new_list, project_id=project_id)
        else:
            for key, sub in enumerate(new_list):
                if sub['linked_from'] != "":
                    keys = self.find_linked_from_key(element_list, sub['linked_from'])
                    if keys != "error_string":
                        if not self.find_name(new_list[keys]['children'], sub['name']):
                            new_list[keys]['children'].append(sub)
                            del new_list[key]
            if len(new_list) == 0:
                new_list = element_list
            self.final_checking(new_list, "base")
            self.three_template = new_list


    def get_element_by_name(self, listing, name):
        for element in listing:
            if element['name'] == name:
                return element
        return False

    def final_checking(self, listing, name):
        for key, element in enumerate(listing):
            if "group_by" in element:
                if self.find_name(object_list=listing, name=element['group_by']) and element['group_by'] != name:
                    getting = self.get_element_by_name(listing, element['group_by'])
                    if "children" in getting:
                        found = 0
                        for childs in getting['children']:
                            if childs['name'] == element['name']:
                                found = 1
                                del listing[key]
                        if found == 0:
                            getting['children'].append(element)
                            del listing[key]

            if "children" in element:
                if len(element['children']) > 0:
                    self.final_checking(element['children'], element['name'])




    def find_name(self, object_list, name):
        for element in object_list:
            if element['name'] == name:
                return True
        return False

    def generate_linked(self, app_id, project_id):
        element_list = []
        collection_subject = self.database.projects_elements
        select_subjects = collection_subject.find(
            {'project_id': project_id, 'app_id': app_id, 'element_type': "subject"}, {"_id": False})
        select_subjects = list(select_subjects)
        for subject in select_subjects:
            group_by = ""
            if "group_by" in subject:
                group_by = subject['group_by']
            template = {
                'name': subject['element_text']['text'],
                'element_id': subject['element_id'],
                'attributes': {
                    'type': subject['element_text']['type']
                },
                'linked_from': subject['linked_from'],
                'group_by': group_by,
                'children': []
            }
            template['nodeSvgShape'] = {}
            template['nodeSvgShape']['shape'] = 'circle'
            template['nodeSvgShape']['shapeProps'] = {}
            template['nodeSvgShape']['shapeProps']['fill'] = '#e67e00'
            template['nodeSvgShape']['shapeProps']['cy'] = 0
            template['nodeSvgShape']['shapeProps']['cx'] = 0
            template['nodeSvgShape']['shapeProps']['r'] = 7
            element_list.append(template)
        self.get_linked_from(element_list=element_list, already_checked=[], new_list=[],project_id=project_id)

    def view_project_three(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }
        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']

        if auth_token == "" or app_id == "" or project_id == "":
            return {
                'msg': "Please complete required field.",
                'status': "forbidden"
            }

        collection_users = self.database.users
        check_user = collection_users.find({'auth_token': auth_token, 'app_id': app_id}, {"_id": False})
        if check_user.count() < 1:
            return {
                'msg': "You can't access here.",
                'status': "forbidden"
            }

        collection_project = self.database.projects
        check_project = collection_project.find({'project_id': project_id, 'app_id': app_id}, {"_id": False})
        if check_project.count() < 1:
            return {
                'msg': "Project not found.",
                'status': "forbidden"
            }
        check_project = list(check_project)[0]

        collection_subject = self.database.projects_elements
        select_subjects = collection_subject.find(
            {'project_id': project_id, 'app_id': app_id, 'element_type': "subject"}, {"_id": False})
        select_subjects = list(select_subjects)

        collection_tasks = self.database.running_modules
        select_tasks = collection_tasks.find({'project_id': project_id, 'app_id': app_id}, {"_id": False}).sort(
            'created_at', DESCENDING).limit(5)
        select_tasks = list(select_tasks)

        project_information = {}
        project_information['name'] = check_project['project_name']
        project_information['attributes'] = {
            'created_at': check_project['created_at'],
            'created_by': check_project['created_by']
        }
        project_subject_tpl = []
        if len(select_subjects) < 1:
            project_information['children'] = []
            project_information['nodeSvgShape'] = {}
            project_information['nodeSvgShape']['shape'] = 'circle'
            project_information['nodeSvgShape']['shapeProps'] = {}
            project_information['nodeSvgShape']['shapeProps']['fill'] = '#e67e00'
            project_information['nodeSvgShape']['shapeProps']['cx'] = 0
            project_information['nodeSvgShape']['shapeProps']['cy'] = 0
            project_information['nodeSvgShape']['shapeProps']['r'] = 7
        else:
            project_information['nodeSvgShape'] = {}
            project_information['nodeSvgShape']['shape'] = 'circle'
            project_information['nodeSvgShape']['shapeProps'] = {}
            project_information['nodeSvgShape']['shapeProps']['fill'] = '#e67e00'
            project_information['nodeSvgShape']['shapeProps']['cx'] = 0
            project_information['nodeSvgShape']['shapeProps']['cy'] = 0
            project_information['nodeSvgShape']['shapeProps']['r'] = 7
            inserted_sujects = []
            for subject in select_subjects:
                subject_tpl = {}
                subject_tpl['name'] = subject['element_text']['text']
                key_count = 0
                if subject['linked_from'] in inserted_sujects:
                    for subject_found in project_subject_tpl:
                        if subject_found['name'] == subject['linked_from']:
                            inserted_sujects.append(subject['element_text']['text'])
                            subject_tpl['attributes'] = {
                                'type': subject['element_text']['type']
                            }
                            subject_tpl['children'] = []
                            subject_tpl['nodeSvgShape'] = {}
                            subject_tpl['nodeSvgShape']['shape'] = 'circle'
                            subject_tpl['nodeSvgShape']['shapeProps'] = {}
                            subject_tpl['nodeSvgShape']['shapeProps']['fill'] = '#e67e00'
                            subject_tpl['nodeSvgShape']['shapeProps']['cy'] = 0
                            subject_tpl['nodeSvgShape']['shapeProps']['cx'] = 0
                            subject_tpl['nodeSvgShape']['shapeProps']['r'] = 7
                            project_subject_tpl[key_count]['children'].append(subject_tpl)
                        key_count = key_count + 1

                elif not subject['linked_from']:
                    inserted_sujects.append(subject_tpl['name'])
                    subject_tpl['attributes'] = {
                        'type': subject['element_text']['type']
                    }
                    subject_tpl['children'] = []
                    select_module_executed = self.database.running_modules.find({
                        'project_id': project_id,
                        'app_id': app_id,
                        'status': 'executed',
                        'project_subject': subject_tpl['name']
                    }, {'_id': False})
                    if(select_module_executed).count() < 1:
                        subject_tpl['children'] = []
                    else:
                        subject_tpl['nodeSvgShape'] = {}
                        subject_tpl['nodeSvgShape']['shape'] = 'circle'
                        subject_tpl['nodeSvgShape']['shapeProps'] = {}
                        subject_tpl['nodeSvgShape']['shapeProps']['fill'] = '#e67e00'
                        subject_tpl['nodeSvgShape']['shapeProps']['cy'] = 0
                        subject_tpl['nodeSvgShape']['shapeProps']['cx'] = 0
                        subject_tpl['nodeSvgShape']['shapeProps']['r'] = 7
                        select_module_executed = list(select_module_executed)
                        module_children = []
                        for module in select_module_executed:
                            module_tpl = {
                                'name': module['module_name'].rsplit('.', 1)[1],
                            }
                            module_tpl['nodeSvgShape'] = {}
                            module_tpl['nodeSvgShape']['shape'] = 'circle'
                            module_tpl['nodeSvgShape']['shapeProps'] = {}
                            module_tpl['nodeSvgShape']['shapeProps']['fill'] = 'grey'
                            module_tpl['nodeSvgShape']['shapeProps']['cy'] = 0
                            module_tpl['nodeSvgShape']['shapeProps']['cx'] = 0
                            module_tpl['nodeSvgShape']['shapeProps']['r'] = 7
                            if "module_export_primary" not in module:
                                module_tpl['attributes'] = {
                                    'result': len(module['results'])
                                }

                            elif module['module_export_primary'] == "":
                                module_tpl['attributes'] = {
                                    'result': len(module['results'])
                                }

                            elif len(module['results']) > 0 and module['module_export_primary'] != "":
                                module_tpl['nodeSvgShape'] = {}
                                module_tpl['nodeSvgShape']['shape'] = 'circle'
                                module_tpl['nodeSvgShape']['shapeProps'] = {}
                                module_tpl['nodeSvgShape']['shapeProps']['fill'] = '#e67e00'
                                module_tpl['nodeSvgShape']['shapeProps']['cy'] = 0
                                module_tpl['nodeSvgShape']['shapeProps']['cx'] = 0
                                module_tpl['nodeSvgShape']['shapeProps']['r'] = 7
                                module_tpl['attributes'] = {
                                    'result': len(module['results'][0])
                                }
                                result_tpl = []
                                if "positive_results" in module:
                                    for result in module['positive_results'][0]:
                                        result_tpl_personal = {}
                                        for key, value in result.iteritems():
                                            result_tpl_personal['attributes'] = {}
                                            if key == module['module_export_primary'] and value != "":
                                                result_tpl_personal['name'] = value
                                        result_tpl.append(result_tpl_personal)
                                    module_tpl['children'] = result_tpl
                            else:
                                module_tpl['attributes'] = {
                                    'result': len(module['results'])
                                }
                            #module_children.append(module_tpl)
                        #module_node = {}
                        #module_node['name'] = "Module_executed"
                        #module_node['children'] = module_children
                        #subject_tpl['children'].append(module_node)
                    #project_subject_tpl.append(subject_tpl)
        self.generate_linked(app_id, project_id)
        project_information['children'] = self.three_template

        return {
            'status': "success",
            'msg': "Project loaded",
            'three': project_information,
            'tasks': list(select_tasks)
        }

    def insert_project_element(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data or "element_type" not in post_data \
                    or "element_text" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        element_type = post_data['element_type']
        element_text = post_data['element_text']

        collection_users = self.database.users
        collection = self.database.projects
        select_user = collection_users.find({'auth_token': auth_token, 'app_id': app_id})
        if select_user.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        select_user = list(select_user)[0]
        if select_user['user_right'] not in self.write_right:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }
        select_project = collection.find({'app_id': app_id, 'project_id': project_id})
        if select_project.count() < 1:
            return {
                'msg': "This project has not found.",
                'status': "forbidden"
            }

        linked_from = ""
        if "linked_from" in post_data:
            linked_from = post_data['linked_from']

        group_by = ""
        if "group_by" in post_data:
            group_by = post_data['group_by']

        collection_element = self.database.projects_elements
        check_exist = collection_element.find({
            'project_id': project_id,
            'app_id': app_id,
            'element_type': element_type,
            'element_text': element_text,
            'linked_from': linked_from
        })
        if check_exist.count() > 0:
            return {
                'msg': "This '"+str(element_type)+"' as already found.",
                'status': "forbidden"
            }

        collection_element.insert({
            'project_id': project_id,
            'app_id': app_id,
            'linked_from': linked_from,
            'element_type': element_type,
            'element_text': element_text,
            'element_id': self.random_element(size=6, prefix=project_id + "_" + app_id + "_"),
            'group_by': group_by
        })

        return {
            'msg': "'"+element_type+"' successfully inserted",
            'status': "success",
            'executed_at': self.get_date()
        }

    def select_project_element(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data or "element_type" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        element_type = post_data['element_type']

        collection_users = self.database.users
        collection = self.database.projects
        select_user = collection_users.find({'auth_token': auth_token, 'app_id': app_id})
        if select_user.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        select_user = list(select_user)[0]
        if select_user['user_right'] not in self.write_right:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }
        select_project = collection.find({'app_id': app_id, 'project_id': project_id})
        if select_project.count() < 1:
            return {
                'msg': "This project has not found.",
                'status': "forbidden"
            }

        collection_element = self.database.projects_elements
        check_exist = collection_element.find({
            'project_id': project_id,
            'app_id': app_id,
            'element_type': element_type,
        }, {"_id": False})

        return {
            'msg': "",
            'status': "success",
            'results': list(check_exist),
            'executed_at': self.get_date()
        }

    def select_project_theme(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data or "element_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

        element_id = post_data['element_id']
        project_id = post_data['project_id']
        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        collection_element = self.database.projects_elements
        result_element = collection_element.find({'element_id': element_id, 'project_id': project_id, 'app_id': app_id})
        if result_element.count() < 1:
            return {
                'msg': "This element has been not found",
                'status': "forbidden"
            }

        collection_users = self.database.users
        if collection_users.find({'auth_token': auth_token, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        element = list(result_element)[0]
        element_tpl = {
            'name': element['element_text']['text'],
            'type': element['element_text']['type'],
            'id': element['element_id']
        }
        collection_modules = self.database.modules
        list_module = collection_modules.find({'module_type': element['element_text']['type']}, {"_id": False, "module_path": False})
        return {
            'status': "success",
            'modules': list(list_module),
            'subject': element_tpl,
            'executed_at': self.get_date()
        }

    def select_module_information(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "module_import" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        module_import = post_data['module_import']
        collection_users = self.database.users
        if collection_users.find({'auth_token': auth_token, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        collection_modules = self.database.modules
        select_module = collection_modules.find({'module_import': module_import}, {"_id": False, "module_path": False})
        if select_module.count() < 1:
            return {
                'msg': "This module has been not found.",
                'status': "forbidden"
            }

        return {
            'msg': "Module found.",
            'status': "success",
            'module': list(select_module)[0]
        }

    def select_project_tasks(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        collection_users = self.database.users
        if collection_users.find({'auth_token': auth_token, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        collection_projects = self.database.projects
        if collection_projects.find({'project_id': project_id, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        select_task = self.database.running_modules.find({'project_id': project_id}, {"_id": False}).sort("created_at", DESCENDING)
        return {
            'status': "success",
            'msg': 'tasks returned.',
            'tasks': list(select_task)
        }

    def select_project_task_unique(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data or "task_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        task_id = post_data['task_id']
        collection_users = self.database.users
        if collection_users.find({'auth_token': auth_token, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        collection_projects = self.database.projects
        if collection_projects.find({'project_id': project_id, 'app_id': app_id}).count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        select_task = self.database.running_modules.find({'project_id': project_id, 'task_id': task_id}, {"_id": False})
        if select_task.count() < 1:
            return {
                'msg': "This task has been not found.",
                'status': "forbidden",
            }
        return {
            'status': "success",
            'msg': 'tasks returned.',
            'task': list(select_task)[0]
        }

    def delete_project_element(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data or "element_id" not in post_data \
                or "element_type" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }
        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        element_type = post_data['element_type']
        project_id = post_data['project_id']
        element_id = post_data['element_id']
        collection_users = self.database.users
        collection = self.database.projects
        select_user = collection_users.find({'auth_token': auth_token, 'app_id': app_id})
        if select_user.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }

        select_user = list(select_user)[0]
        if select_user['user_right'] not in self.write_right:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }
        select_project = collection.find({'app_id': app_id, 'project_id': project_id})
        if select_project.count() < 1:
            return {
                'msg': "This project has not found.",
                'status': "forbidden"
            }
        collection_element = self.database.projects_elements
        check_exist = collection_element.find({
            'project_id': project_id,
            'app_id': app_id,
            'element_type': element_type,
            'element_id': element_id
        }, {"_id": False})
        if check_exist.count() > 0:
            collection_element.remove({
                'project_id': project_id,
                'app_id': app_id,
                'element_type': element_type,
                'element_id': element_id
            })
            return {
                'msg': "Element successfully removed.",
                'status': 'success'
            }
        else:
            return {
                'msg': "'"+str(element_type)+"' not found",
                'status': 'forbidden'
            }

    def update_result_false_flag(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data or "task_id" not in post_data \
                or "result_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }

    def export_project_to_json(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }
        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        collection_users = self.database.users
        collection = self.database.projects
        select_user = collection_users.find({'auth_token': auth_token, 'app_id': app_id})
        if select_user.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }
        select_project = collection.find({'app_id': app_id, 'project_id': project_id})
        if select_project.count() < 1:
            return {
                'msg': "This project has not found.",
                'status': "forbidden"
            }

        select_project = list(select_project)[0]

        json_template = {
            "project":{
                "name": select_project['project_name'],
                "created_at": select_project['created_at'],
                "created_by": select_project['created_by'],
                "subjects": [],
                "notes": []
            }
        }

        select_subject = self.database.projects_elements.find(
            {
                'project_id': select_project['project_id'],
                'element_type': 'subject',
                'app_id': app_id
            },
            {
                '_id': False,
                'app_id': False,

            }
        )

        select_subject = list(select_subject)
        for subject in select_subject:
            subject_tpl = {
                "name": subject['element_text']['text'],
                "type": subject['element_text']['type'],
                "module_executed": []
            }
            select_module = self.database.running_modules.find(
                {
                    "project_id": project_id,
                    "app_id": app_id,
                    "project_subject": subject['element_text']['text']
                },
                {
                    '_id': False,
                    'app_id': False,
                    'module_export_primary': False
                }
            )
            if select_module.count() > 0:
                module_count =  []
                for module in select_module:
                    module_tpl = {
                        "module_name": module['module_name'],
                        "module_result": module['results'],
                        "module_output": module['module_output']
                    }
                    module_count.append(module_tpl)
                subject_tpl["module_executed"] = module_count
            json_template["project"]["subjects"].append(subject_tpl)
        select_note = self.database.projects_elements.find(
            {
                'project_id': select_project['project_id'],
                'element_type': 'note',
                'app_id': app_id
            },
            {
                '_id': False,
                'app_id': False,

            }
        )
        for note in select_note:
            note_tpl = {
                "note_subject_type": note['element_text']['subject_type'],
                "note_text": note['element_text']['note_text'],
                "note_subject": note['element_text']['subject']
            }
            json_template["project"]["notes"].append(note_tpl)
        return json_template

    def export_project_to_xml(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data:
            return {
                    'msg': "Please complete required field.",
                    'status': "forbidden"
                }
        auth_token = post_data['u_auth_token']
        app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        collection_users = self.database.users
        collection = self.database.projects
        select_user = collection_users.find({'auth_token': auth_token, 'app_id': app_id})
        if select_user.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }
        select_project = collection.find({'app_id': app_id, 'project_id': project_id})
        if select_project.count() < 1:
            return {
                'msg': "This project has not found.",
                'status': "forbidden"
            }

        select_project = list(select_project)[0]

        json_template = {
            "project":{
                "name": select_project['project_name'],
                "created_at": select_project['created_at'],
                "created_by": select_project['created_by'],
                "subjects": [],
                "notes": []
            }
        }

        select_subject = self.database.projects_elements.find(
            {
                'project_id': select_project['project_id'],
                'element_type': 'subject',
                'app_id': app_id
            },
            {
                '_id': False,
                'app_id': False,

            }
        )

        select_subject = list(select_subject)
        for subject in select_subject:
            subject_tpl = {
                "name": subject['element_text']['text'],
                "type": subject['element_text']['type'],
                "module_executed": []
            }
            select_module = self.database.running_modules.find(
                {
                    "project_id": project_id,
                    "app_id": app_id,
                    "project_subject": subject['element_text']['text']
                },
                {
                    '_id': False,
                    'app_id': False,
                    'module_export_primary': False
                }
            )
            if select_module.count() > 0:
                module_count =  []
                for module in select_module:
                    module_tpl = {
                        "module_name": module['module_name'],
                        "module_result": module['results'],
                        "module_output": module['module_output']
                    }
                    module_count.append(module_tpl)
                subject_tpl["module_executed"] = module_count
            json_template["project"]["subjects"].append(subject_tpl)
        select_note = self.database.projects_elements.find(
            {
                'project_id': select_project['project_id'],
                'element_type': 'note',
                'app_id': app_id
            },
            {
                '_id': False,
                'app_id': False,

            }
        )
        for note in select_note:
            note_tpl = {
                "note_subject_type": note['element_text']['subject_type'],
                "note_text": note['element_text']['note_text'],
                "note_subject": note['element_text']['subject']
            }
            json_template["project"]["notes"].append(note_tpl)
        parsed = parseString(dicttoxml(json_template,ids=True, attr_type=False))
        return {
            'export': parsed.toprettyxml()
        }

    def remove_project(self, post_data):
        if "u_auth_token" not in post_data or "u_app_id" not in post_data \
                or "project_id" not in post_data:
            return {
                'msg': "Please complete required field.",
                'status': "forbidden"
            }
        u_auth_token = post_data['u_auth_token']
        u_app_id = post_data['u_app_id']
        project_id = post_data['project_id']
        collection_users = self.database.users
        collection = self.database.projects
        select_user = collection_users.find({'auth_token': u_auth_token, 'app_id': u_app_id})
        if select_user.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }
        find_project = collection.find({'project_id': project_id, 'app_id': u_app_id})
        if find_project.count() < 1:
            return {
                'msg': "You don't have access right.",
                'status': "forbidden"
            }
        collection.remove({'project_id': project_id, 'app_id': u_app_id})
        return {
            'msg': "Project successfully deleted",
            'status': 'success'
        }












