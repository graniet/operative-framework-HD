import React from 'react'
import axios from 'axios'
import Config from '../../../Config'

const SERVER_ADDR = Config();


class EngineBreach extends React.Component {

    static breachInformation() {
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        if (userToken !== undefined) {
            return axios.post(SERVER_ADDR + '/breach/informations', {
                'u_auth_token': userToken,
                'u_app_id': userApp,
            }).then(res => {
                return res.data
            })
        }
    }

    static breachSearch(searchText, searchType){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        if (userToken !== undefined) {
            return axios.post(SERVER_ADDR + '/breach/search', {
                'u_auth_token': userToken,
                'u_app_id': userApp,
                'searchText': searchText,
                'searchType': searchType
            }).then(res => {
                return res.data
            })
        }
    }
}

export default EngineBreach