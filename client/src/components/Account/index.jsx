import React from "react";
import styled from "styled-components"
import Message from '../Message'
import axios from 'axios'
import Config from '../Config'

import { Redirect } from 'react-router-dom'


const Screen = styled.div`
        .buttonBasic{
            box-shadow: 0 0 0 0 !important;
            border-bottom: 3px solid #e77d03;
            border-left: 1px solid #ffffff !important;
            border-radius: 0 !important;
            background: #fafafa !important;
            color: #4e2b01 !important;
        }
        
`;

const SERVER_ADDR = Config();


export class Login extends React.Component{


    constructor(props) {
        super(props);
        this.state = {
            user_name: "",
            user_password: "",
            user_logged: false,
            user_message: "",
            user_messageStatus: "",
        };

        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
        this.handleSubmitForm = this.handleSubmitForm.bind(this)
    }

    handleUsernameChange(e){
        this.setState({user_name: e.target.value});
        localStorage.setItem("user_name", e.target.value);
    }

    handlePasswordChange(e){
        this.setState({user_password: e.target.value});
    }

    handleSubmitForm(e){
        axios.post(SERVER_ADDR +"/auth/user/login", {"u_name": this.state.user_name, "u_password": this.state.user_password})
            .then(res => {
                if(res.data.auth_token !== undefined && res.data.status === "success"){
                    localStorage.clear();
                    localStorage.setItem('operativeAuthToken', res.data.auth_token);
                    localStorage.setItem('operativeApp', res.data.app_id);
                    this.setState({ user_logged: true });
                }
                else if(res.data.msg !== undefined){
                    this.setState({
                        user_message: res.data.msg,
                        user_messageStatus: "negative"
                    });
                }
                else{
                    this.setState({
                        user_message: "Error as been found.",
                        user_messageStatus: "yellow"
                    })
                }
            });
        e.preventDefault();
    }

    render(){
        if(this.state.user_logged === true){
            return <Redirect to="/account"/>
        }
        return (
            <Screen>
                <Message userMessage={this.state.user_message} userStatus={this.state.user_messageStatus}/>
                <form className="ui form" onSubmit={this.handleSubmitForm}>
                    <div className="field">
                        <label>Username</label>
                        <input type="text" placeholder="username" value={this.state.user_name} onChange={this.handleUsernameChange}/>
                    </div>
                    <div className="field">
                        <label>Password</label>
                        <input type="password" placeholder="******" value={this.state.user_password} onChange={this.handlePasswordChange}/>
                    </div>
                    <div className="field">
                        <input type="submit" className={"ui button buttonBasic"} value="Login" />
                    </div>
                </form>
            </Screen>
        )
    }
}

export const Logout = () => {
    localStorage.clear();
    return <Redirect to="/login" />
};


export default Login