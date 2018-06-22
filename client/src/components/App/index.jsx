import React from "react";
import styled, {injectGlobal} from "styled-components"
import Login, {Logout} from '../Account'
import RouteAuth from '../RouteAuth'
import RouteNoAuth from '../RouteNoAuth'
import Nav from '../Nav'
import Module, {UseModule} from '../Module'
import Tasks, { ViewTask } from '../Task'
import Teams, { AddMember } from '../Teams'
import ViewBreach from '../Breach'
import Projects, { ViewProjectSubjects, ExportProjectXml, ExportProjectJson, AddProject, ViewProject, ViewProjectThree, ViewProjectTask } from '../Projects'
import { BrowserRouter as Router, Switch } from "react-router-dom";

injectGlobal`
body{
    margin: 0 !important;
}
`;

const Container = styled.div`
    margin: 0 !important;
    width: 100%;
`;

const Content = {
    marginTop: "30px",
    clear: "both",
    width: "90%",
    marginRight: "auto",
    marginLeft: "auto",
    borderRadius: "0",
};

class App extends React.Component{

    constructor(props){
        super(props);
        this.state = {
            moduleList: [],
            moduleCount: 0,
            userLogged: false,
        }
    }


    render(){
        return(
            <Router>
                <Container>
                    <Nav/>
                    <div style={Content}>
                        <Switch>
                            <RouteNoAuth exact path="/login" component={Login} loggedIn={this.state.userLogged}/>
                            <RouteAuth exact path="/logout" component={Logout}/>
                            <RouteAuth exact path="/" component={Projects}/>
                            <RouteAuth exact path="/account" component={Projects}/>
                            <RouteAuth exact path="/modules" component={Module}/>
                            <RouteAuth exact path="/m/info/:moduleImport" component={UseModule}/>
                            <RouteAuth exact path="/tasks" component={Tasks}/>
                            <RouteAuth exact path="/task/view/:taskId" component={ViewTask}/>
                            <RouteAuth exact path={"/teams"} component={Teams}/>
                            <RouteAuth exact path={"/teams/add"} component={AddMember}/>
                            <RouteAuth exact path={"/projects"} component={Projects}/>
                            <RouteAuth exact path={"/project/add"} component={AddProject}/>
                            <RouteAuth exact path={"/project/view/:projectId"} component={ViewProject}/>
                            <RouteAuth exact path={"/project/view/three/:projectId"} component={ViewProjectThree}/>
                            <RouteAuth exact path={"/project/view/:projectId/:taskId"} component={ViewProjectTask}/>
                            <RouteAuth exact path={"/project/:projectId/export/json"} component={ExportProjectJson}/>
                            <RouteAuth exact path={"/project/:projectId/export/xml"} component={ExportProjectXml}/>
                            <RouteAuth exact path={"/project/:projectId/subjects"} component={ViewProjectSubjects}/>
                            <RouteAuth exact path={"/project/:projectId/breach"} component={ViewBreach}/>
                        </Switch>
                    </div>
                </Container>
            </Router>
        );
    }
}




export default App;