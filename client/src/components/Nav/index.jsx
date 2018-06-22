import React from 'react'
import styled from "styled-components"
import Logo from '../../assets/logo.png'
import authMiddleware from '../Middleware'
import { Link } from "react-router-dom";

const listMainRight = {
    listStyle: 'none',
    display: 'flex',
    margin: '0',
    float: 'right',
    padding: '0',
    paddingTop: '12px',
};

const listMain = {
    listStyle: 'none',
    display: 'flex',
    margin: '0',
    float: 'left',
    padding: '0',
    paddingTop: '12px',
};

const listLiMain = {
    fontFamily: "sans-serif",
    paddingRight: '10px',
    fontSize: '13px',
    textDecoration: 'none',
    color: 'black',
};

const listLiMain2 = {
    fontFamily: "sans-serif",
    paddingRight: '10px',
    fontSize: '13px',
    textDecoration: 'none',
    color: 'black',
    borderRight: '1px solid #292c34',
    paddingLeft: '10px',
};

const listLiMainRight = {
    fontFamily: "sans-serif",
    paddingRight: '10px',
    fontSize: '13px',
    textDecoration: 'none',
    color: 'black',
    borderLeft: '1px solid #292c34',
    paddingLeft: '10px',
};

const MenuBar = styled.div`
    border-bottom: 1px solid #908d8d;
    border-top: 3px solid #e67e00;
    width: 100%;
    height: 40px;
    padding-left: 5px;
    box-shadow: 1px 1px 1px 1px #b7b7b7;
`;

const MenuBarProject = styled.div`
    border-bottom: 1px solid #908d8d;
    width: 100%;
    height: 40px;
    padding-left: 5px;
    margin-bottom: 15px;
`;

const MenuBarLogin = styled.div`
    border-bottom: 1px solid #908d8d;
    border-top: 3px solid #e67e00;
    width: 100%;
    height: 40px;
    padding-left: 5px;
    box-shadow: 1px 1px 1px 1px #b7b7b7;
`;

const ClearBoth = styled.div`
    clear: both;
`;

const logoMenu = {
    float: 'left',
    width: '190px'
};


class Nav extends React.Component{

    render(){

        if(authMiddleware()){
            return(
                <MenuBar>
                    <img alt="operative logo" style={logoMenu} src={Logo} />
                    <ul style={listMain}>
                        <Link to="/projects" style={listLiMain}><i className={"fas fa-project-diagram"}></i> Projects</Link>
                        <Link to="/modules" style={listLiMain}><i className={"fas fa-th-list"}></i> Modules</Link>
                        <Link to="/tasks" style={listLiMain}><i className={"fas fa-th-list"}></i> Results</Link>
                    </ul>
                    <ul style={listMainRight}>
                        <Link to="/teams" style={listLiMain}><i className={"fas fa-users"}></i> Team</Link>
                        <Link to="/logout" style={listLiMain}><i className={"fas fa-sign-out-alt"}></i> Logout</Link>
                    </ul>
                </MenuBar>
            )
        }
        else{
            return(
                <MenuBarLogin>
                    <img alt="operative logo" style={logoMenu} src={Logo} />
                    <ul style={listMainRight}>
                        <Link to="/login" style={listLiMain}><i className={"fas fa-sign-in-alt"}></i> Login</Link>
                    </ul>
                </MenuBarLogin>
            )
        }
    }
}

export class NavProject extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            'project_id': props.projectId
        }
    }

    render(){
        return (
            <div>
            <MenuBarProject>
                <ul style={listMain}>
                    <Link to={"/project/view/" + this.state.project_id} style={listLiMain2}>
                        <i className="far fa-play-circle"></i> Basic view
                    </Link>
                    <Link to={"/project/view/three/" + this.state.project_id} style={listLiMain2}>
                        <i className="fas fa-code-branch"></i> Graphical view
                    </Link>
                    <Link to={"/project/" + this.state.project_id + "/subjects"} style={listLiMain2}>
                        <i className="far fa-lightbulb"></i> Subjects
                    </Link>
                    <Link to={"/"} style={listLiMain2}>
                        <i className="far fa-comment"></i> Notes
                    </Link>
                    <Link to={"/project/"+this.state.project_id+"/breach"} style={listLiMain2}>
                        <i className="fab fa-searchengin"></i> Public breach
                    </Link>
                </ul>
                <ul style={listMainRight}>
                    <Link to={"/project/"+this.state.project_id+"/export/xml"} style={listLiMainRight}>
                        <i className="fas fa-download"></i> XML
                    </Link>
                    <Link to={"/project/"+this.state.project_id+"/export/json"} style={listLiMainRight}>
                        <i className="fas fa-download"></i> JSON
                    </Link>
                    <Link to={"/project/"+this.state.project_id+"/export/json"} style={listLiMainRight}>
                        <i className="fas fa-download"></i> PDF
                    </Link>
                </ul>
            </MenuBarProject>
                <ClearBoth />
            </div>
        )
    }
}


export default Nav;