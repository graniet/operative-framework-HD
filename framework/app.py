#!/usr/bin/env  python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, render_template, request
import config

from engine import database

app = Flask(__name__)
db = database.Engine(config.MONGODB_HOST, config.MONGODB_PORT)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def page_not_allowed(e):
    return render_template('405.html'), 405


@app.route('/')
def all():
    return jsonify(
        {
            "message": "Welcome to Operative API"
        }
    )


@app.route('/module/<module_import>', methods=['GET'])
def module_information(module_import):
    return jsonify(db.module_information(module_import=module_import))


@app.route('/module/use/<module_import>/<auth_token>', methods=['POST'])
def module_execute(module_import, auth_token):
    return jsonify(db.execute_module(auth_token=auth_token, module_import=module_import, post_data=request.get_json()))


@app.route('/module/all', methods=['GET'])
def get_modules_all():
    return jsonify(db.select_module(limit="*"))


@app.route('/module/task/<task_id>', methods=['GET'])
def task_view(task_id):
    return jsonify(db.task_view(task_id))


@app.route('/view/task/<auth_token>', methods=['GET'])
def view_task(auth_token):
    return jsonify(db.task_all(auth_token))


@app.route('/auth/user/login', methods=['POST'])
def auth_login():
    return jsonify(db.login_user(post_data=request.get_json()))


@app.route('/auth/user/register', methods=['POST'])
def auth_register():
    return jsonify(db.register_user(post_data=request.get_json()))


@app.route('/team/add/member', methods=['POST'])
def register_user_team():
    return jsonify(db.register_user_team(post_data=request.get_json()))


@app.route('/team/delete/member', methods=['POST'])
def remove_user_team():
    return jsonify(db.remove_user_team(post_data=request.get_json()))


@app.route('/auth/check/<auth_token>/<app_id>', methods=['GET'])
def check_login(auth_token, app_id):
    return jsonify(db.check_login(auth_token, app_id))


@app.route('/user/account/<user_token>', methods=['GET'])
def user_information(user_token):
    return jsonify(db.user_information(user_token))


@app.route('/view.task/<task_id>/<auth_token>', methods=['GET'])
def view_unique_task(task_id, auth_token):
    return jsonify(db.task_view_unique(task_id=task_id, auth_token=auth_token))


@app.route('/user/teams/<auth_token>/<app_id>', methods=['GET'])
def view_teams(auth_token, app_id):
    return jsonify(db.get_teams(auth_token=auth_token, app_id=app_id))


@app.route('/project/create', methods=['POST'])
def create_project():
    return jsonify(db.create_project(post_data=request.get_json()))


@app.route('/project/lists/<auth_token>/<app_id>', methods=['GET'])
def list_projects(auth_token, app_id):
    return jsonify(db.list_projects(auth_token, app_id))


@app.route('/project/view', methods=['POST'])
def view_project():
    return jsonify(db.view_project(post_data=request.get_json()))


@app.route('/project/remove', methods=['POST'])
def remove_project():
    return jsonify(db.remove_project(post_data=request.get_json()))


@app.route('/project/view/three', methods=['POST'])
def view_project_three():
    return jsonify(db.view_project_three(post_data=request.get_json()))


@app.route('/project/element/remove', methods=['POST'])
def delete_project_element():
    return jsonify(db.delete_project_element(post_data=request.get_json()))


@app.route('/project/insert', methods=['POST'])
def insert_project_element():
    return jsonify(db.insert_project_element(post_data=request.get_json()))


@app.route('/project/select', methods=['POST'])
def select_project_element():
    return jsonify(db.select_project_element(post_data=request.get_json()))


@app.route('/project/select/theme', methods=['POST'])
def select_project_theme():
    return jsonify(db.select_project_theme(post_data=request.get_json()))


@app.route('/project/select/module', methods=['POST'])
def select_module_information():
    return jsonify(db.select_module_information(post_data=request.get_json()))


@app.route('/project/run/module', methods=['POST'])
def execute_project_module():
    return jsonify(db.execute_project_module(post_data=request.get_json()))


@app.route('/project/select/tasks', methods=['POST'])
def select_project_tasks():
    return jsonify(db.select_project_tasks(post_data=request.get_json()))


@app.route('/project/export/json', methods=['POST'])
def export_project_to_json():
    return jsonify(db.export_project_to_json(post_data=request.get_json()))


@app.route('/project/export/xml', methods=['POST'])
def export_project_to_xml():
    return jsonify(db.export_project_to_xml(post_data=request.get_json()))


@app.route('/project/select/task', methods=['POST'])
def select_project_task_unique():
    return jsonify(db.select_project_task_unique(post_data=request.get_json()))


@app.route('/breach/informations', methods=['POST'])
def breach_information():
    return jsonify(db.breach_information(post_data=request.get_json()))


@app.route('/breach/search', methods=['POST'])
def breach_search():
    return jsonify(db.breach_search(post_data=request.get_json()))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=config.BACKEND_PORT)
