import React from 'react'
import axios from 'axios'
import Config from '../../../Config'

const SERVER_ADDR = Config();

class EngineProjects extends React.Component{

    static createProject(project_name){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        if(project_name !== undefined){
            return axios.post(SERVER_ADDR + '/project/create',{
                'u_auth_token': userToken,
                'u_app_id': userApp,
                'project_name': project_name
            }).then(res => {
                return res.data
            })
        }
    }

    static removeProject(project_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/remove', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id
        }).then(res => {
            return res.data
        })
    }

    static listProjects(userT, userA){
        return axios.get(SERVER_ADDR + '/project/lists/' + userT + '/' + userA)
            .then(res => {
                return res.data
            })
    }

    static loadProjects(project_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/view', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id
        })
            .then(res => {
                return res.data
            })
            .catch(res => {
                return {
                    'status': "forbidden",
                    'msg': "A error as occurred"
                }
            })
    }

    static loadProjectsThree(project_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/view/three', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id
        })
            .then(res => {
                return res.data
            })
            .catch(res => {
                return {
                    'status': "forbidden",
                    'msg': "A error as occurred"
                }
            })
    }

    static insertProjectElement(project_id, element_type, element_text){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/insert', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
            'element_type': element_type,
            'element_text': element_text
        })
            .then(res => {
                return res.data
            })
    }

    static insertProjectElementFrom(project_id, element_type, element_text, from_text, group_by){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/insert', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
            'element_type': element_type,
            'element_text': element_text,
            'linked_from': from_text,
            'group_by': group_by
        })
            .then(res => {
                return res.data
            })
    }

    static removeProjectElement(project_id, element_type, element_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/element/remove', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
            'element_type': element_type,
            'element_id': element_id
        })
            .then(res => {
                return res.data
            })
    }

    static selectProjectElement(project_id, element_type){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/select', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
            'element_type': element_type,
        })
            .then(res => {
                return res.data
            })
    }

    static selectProjectThemes(project_id, element_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/select/theme', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
            'element_id': element_id,
        })
            .then(res => {
                return res.data
            })
    }

    static selectProjectModule(module_import){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/select/module', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'module_import': module_import,
        })
            .then(res => {
                return res.data
            })
    }

    static getProjectTask(project_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/select/tasks', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
        })
            .then(res => {
                return res.data
            })
    }

    static getProjectTaskUnique(project_id, task_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/select/task', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
            'task_id': task_id
        })
            .then(res => {
                return res.data
            })
    }

    static exportProjectJson(project_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/export/json', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
        })
            .then(res => {
                return res.data
            })
    }

    static exportProjectXml(project_id){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/export/xml', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'project_id': project_id,
        })
            .then(res => {
                return res.data
            })
    }
}

export default EngineProjects