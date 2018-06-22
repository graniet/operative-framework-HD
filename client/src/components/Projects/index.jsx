import React from 'react'
import EngineProjects from '../Database/Engine/Projects'
import EngineModules from '../Database/Engine/Modules'
import styled from 'styled-components'
import Message from '../Message'
import {Link} from 'react-router-dom'
import Tree from 'react-d3-tree';
import {NavProject} from '../Nav'
import Highlight from 'react-highlight'

const tableTeam = {
    background: "#fafafa",
    borderRadius: "0 !important",
    boxShadow: "0 0 0 0",
};
const containerStyles = {
    width: '100%',
    height: '100%',
};

const Screen = styled.div`
        .buttonBasic{
            box-shadow: 0 0 0 0 !important;
            border-bottom: 3px solid #e77d03;
            border-left: 1px solid #ffffff !important;
            border-radius: 0 !important;
            background: #bbbbbb87 !important;
            color: #4e2b01 !important;
        }
        .formArgument{
            border-radius: 0 0 0 0;
            background-color: #b1b1b121 !important;
            
        }
        .requiredInput{
            color: orange !important;
            text-transform: none;
        }
        .executeQuote{
            font-size: 0.7em;
        }
        small{
            color: #8f8d8d;
            font-size: 0.8em;
        }
        .subjectList{
            margin-top: 10px;
            max-height: 230px;
        }
        .tablesubject{
            border: 0 !important;
        }
        #style1::-webkit-scrollbar {
            width: 6px;
            background-color: #00000;
        } 
        #style1::-webkit-scrollbar-thumb {
            background-color: #e77d03;
            border-radius: 0 0 0 0;
        }
        .selectionable{
            cursor: pointer;
        }
        .noradius{
            border-radius: 0 0 0 0;
        }
        .secondaryOperative{
            border: 0;
            width: 100%;
            height: 40px;
            border-radius: 0 0 0;
            padding-left: 5px;
            box-shadow: 0 0 0 0;
            background: #ffffff;
            border-top: 0;
        }
        .displayNone{
            display: none !important;
        }
        .secondaryOperative .item{
            border: 0;
            border-bottom: 2px solid #e77d03;
            border-radius: 0 !important;
            margin-right: 5px;
        
        }
        .secondaryOperative .item:before{
            background: none !important;
        
        }
        .secondaryOperativeIcon{
            margin-right: 5px;
            font-size: 0.8em;
        }
        .sixcol{
            border: 3px solid #f7f7f7;
            margin-top: 10px;
            max-height: 170px;
            padding: 13px;
        }
        .sixcol5{
            background: #dededf1a;
            max-height: 500px
            height: 600px
            border-right: 3px solid #e77d03;
            border-bottom: 3px solid #e77d03;
            
        }
        .sixcol2{
            border: 3px solid #f7f7f7;
            margin-top: 10px;
            padding: 10px;
            max-height: 350px;
        }
        .sixcol3
        {
            background: #dededf1a;
            max-height: 500px
            height: 600px
        }
        .sixcol4{
            border-right: 1px solid #8f8d8d;
            background: #dededf1a;
        }
        .tencol{
            margin-top: 10px;
        }
        .taskcol{
            margin-top: 25px;
        }
        
        .tencol2{
            background: #000000c4;
            max-height: 500px
            height: 500px
            border-bottom: 3px solid #e77d03;
        }
        .tencol_view_task{
            max-height: 500px
            height: 500px
            overflow-y: scroll;
            border-bottom: 3px solid #e77d03;
        }
        
        .tencolmaxheight{
            max-height: 620px;
        }
        .green{
            color: green;
        }
        .red{
            color: red;
        }
        .orange_text{
            color: orange;
        }
        .module_argument_div{
            padding: 5px;
            border-top: 2px solid #e77c04;
        }
        .nodisplay{
            display: none;
        }
        .preHight{
            max-height: 500px;
            overflow-y: scroll;
        }
`;

class Projects extends React.Component{

    constructor(){
        super();
        this.state = {
            'projects': [<tr key="0">
                <td>No projects found.</td>
                <td></td>
                <td></td>
            </tr>],
            'userMessage': "We load your project, please wait...",
            'userStatus': "warning"
        };

        EngineProjects.listProjects(localStorage.getItem('operativeAuthToken'), localStorage.getItem('operativeApp'))
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "negative"
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'userMessage': '',
                            'userStatus': '',
                            'projects': res.projects
                        });
                    }
                }
                else{
                    this.setState({
                        'userMessage':"A error as been occurred.",
                        'userStatus': "negative"
                    })
                }
            });

        this.removeProject = this.removeProject.bind(this);
    }


    removeProject(e){
        let project_id = e.target.dataset.project
        EngineProjects.removeProject(project_id)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "success"){
                        this.setState({
                            'userMessage': 'Project successfully deleted',
                            'userStatus': 'positive'
                        });
                        let el = document.getElementById("list_" + project_id)
                        el.remove()
                    }
                    else{
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                }
                else{
                    this.setState({
                            'userMessage': 'A error as occured',
                            'userStatus': 'negative'
                        })
                }
            })
    }

    projectLists(){
        let rows = [];
        this.state.projects.forEach((project, i) => {
            rows.push(
                <tr key={i} id={"list_" + project.project_id}>
                    <td>{project.project_name}</td>
                    <td>{project.created_by}</td>
                    <td>{project.created_at}</td>
                    <td><Link to={"/project/view/" + project.project_id}><button className={"ui button mini basic buttonBasic"}><i className="fas fa-folder-open"></i></button></Link></td>
                    <td><button data-project={project.project_id} onClick={this.removeProject} className={"ui button mini basic buttonBasic"}><i className="fas fa-trash-alt"></i></button></td>
                </tr>
            )
        });
        return rows
    }

    render(){
        return (
            <Screen>
                <Link to="/project/add" className="ui button basic mini buttonBasic">
                    <i className="fas fa-plus"></i>
                </Link>
                <Message userMessage={this.state.userMessage} userStatus={this.state.userStatus}/>
                <table className="ui basic table orange">
                    <thead style={tableTeam}>
                    </thead>
                    <tbody>
                    {this.projectLists()}
                    </tbody>
                </table>
            </Screen>
        )
    }
}

export class AddProject extends React.Component{

    constructor(){
        super();
        this.state = {
            'project_name':'',
            'userMessage': '',
            'userStatus' : ''
        };

        this.setProjectName = this.setProjectName.bind(this);
        this.createProject = this.createProject.bind(this);
    }

    setProjectName(e){
        this.setState({
            'project_name': e.target.value
        })
    }

    createProject(e){
        let element = document.getElementById('addProject');
        element.classList.add('loading');
        EngineProjects.createProject(this.state.project_name)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'positive'
                        })
                    }
                }
                else{
                    this.setState({
                        'userMessage': "A error has been occured",
                        'userStatus': 'negative'
                    })
                }
                element.classList.remove('loading');
            })
    }

    render(){
        return(
            <Screen>
                <Link to={"/projects"} className={""}>Go to projects</Link>
                <Message userMessage={this.state.userMessage} userStatus={this.state.userStatus}/>
                <div className={"ui segment formArgument"}>
                    <div className={"ui form"}>
                        <div className={"field"}>
                            <label>Name of project</label>
                            <input type={"text"} placeholder={"My project"} onChange={this.setProjectName} />
                        </div>
                    </div>
                </div>
                <button id={"addProject"} className={"ui button orange buttonBasic"} onClick={this.createProject}>Add a project</button>
            </Screen>
        )
    }
}

export class ViewProject extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            'displayed': 'nodisplay',
            'valid_check': 'far fa-check-circle green',
            'waiting_check': 'fas fa-ellipsis-h',
            'search_icon': 'fas fa-ellipsis-h',
            'userMessage': "Please wait, we open a project...",
            'userStatus': "warning",
            'project_subject': [],
            'project_tasks': [],
            'project_info': [],
            'subject_new': '',
            'subject_new_type':'email',
            'project_id': props.match.params.projectId,
            'waiting_subject': 'Please select a subject',
            'waiting_subject_type': '',
            'waiting_subject_icon': 'fas fa-ellipsis-h',
            'waiting_module': 'Please select a module',
            'waiting_module_icon': 'fas fa-ellipsis-h',
            'waiting_status': 'Not started',
            'waiting_status_icon': 'fas fa-ellipsis-h',
            'waiting_subject_status': 'disabled warning',
            'waiting_module_status': 'disabled warning',
            'waiting_status_status': 'disabled warning',
            'run_status': 'disabled',
            'module_selected': '',
            'moduleArguments': [],
            'moduleArgumentsNb': '0',
            'subject_button': ''
        };
        EngineProjects.loadProjects(props.match.params.projectId)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'userMessage': '',
                            'userStatus': '',
                            'project_info': res.projects,
                            'project_tasks': res.tasks,
                            'project_subject': res.subjects,
                            'project_id': props.match.params.projectId,
                            'displayed': ''
                        })
                    }
                }
            });

        this.setSubject = this.setSubject.bind(this);
        this.setSubjectType = this.setSubjectType.bind(this);
        this.insertSubject = this.insertSubject.bind(this);
        this.viewSubject = this.viewSubject.bind(this);
        this.selectSubject = this.selectSubject.bind(this);
        this.loadModulesFromArray = this.loadModulesFromArray.bind(this);
        this.onModuleSelect = this.onModuleSelect.bind(this);
        this.onRunModule = this.onRunModule.bind(this);
        this.listArgument = this.listArgument.bind(this);
        this.onChangeArgument = this.onChangeArgument.bind(this);
        this.listTasks = this.listTasks.bind(this);
        this.loadTasks = this.loadTasks.bind(this);
    }

    componentDidMount() {
        this.counter = setInterval(
            () => this.loadTasks(),
            10000
        );
        this.deleteAlert = setInterval(
            () => {
                if(this.state.userStatus !== '' || this.state.userMessage !== '') {
                    this.setState({
                        'userMessage': '',
                        'userStatus': ''
                    })
                }
            }, 10000
        )
    }

    componentWillUnmount() {
        clearInterval(this.counter);
        clearInterval(this.deleteAlert)
    }

    loadTasks(){
        EngineProjects.getProjectTask(this.state.project_id)
            .then(res => {
                if(res.status === "success" && res.tasks !== undefined){
                    this.setState({
                        'project_tasks': res.tasks,
                    })
                }
            })
    }

    setSubject(e){
        this.setState({
            'subject_new': e.target.value
        })
    }

    setSubjectType(e){
        this.setState({
            'subject_new_type': e.target.value,
            'waiting_subject_type': e.target.value
        })
    }

    viewSubject(){
        let rows = [];
        this.state.project_subject.forEach((element, i) => {
           rows.push(
               <tr key={i}>
                   <td>{element.element_text.text} <small>({element.element_text.type})</small></td>
                   <td className="right aligned selectionable"><button id={"button_subject_" + i} data-buttonname={"button_subject_" + i} data-element={element.element_id} onClick={this.selectSubject} className={"ui button mini basic "}> select <i className="fas fa-angle-double-right executeQuote"></i></button></td>
               </tr>
           )
        });
        return rows
    }

    selectSubject(e){
        let subject_id = e.target.dataset.element;
        let button_subject = e.target.dataset.buttonname;
        let el = undefined;
        if(button_subject !== undefined){
            if(this.state.subject_button !== ""){
                el = document.getElementById(this.state.subject_button);
                if(el !== undefined) {
                    el.innerHTML = 'select <i class="fas fa-angle-double-right executeQuote"></i>';
                }
            }
            el = document.getElementById(button_subject);
            if(el !== undefined){
                el.innerHTML = '<i class="fas fa-spinner fa-pulse"></i>';
            }
            this.setState({
                'subject_button': button_subject,
                'waiting_subject_icon': 'fas fa-spinner fa-pulse',
                'waiting_subject': 'we load a subject...'
            })
        }
        EngineProjects.selectProjectThemes(this.state.project_id, subject_id)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'waiting_subject': res.subject.name,
                            'waiting_subject_type': res.subject.type,
                            'waiting_subject_status': '',
                            'waiting_subject_icon': this.state.valid_check,
                            'waiting_module': <select id={"moduleForSubject"} onChange={this.onModuleSelect} className={"ui dropdown"}>{this.loadModulesFromArray(res.modules)}</select>,
                            'waiting_module_status': '',
                            'moduleArgumentsNb': '0',
                            'search_icon': this.state.valid_check,
                            'moduleArguments': [],
                            'waiting_module_icon': this.state.waiting_check
                        });
                        el = document.getElementById(this.state.subject_button);
                        if(el !== undefined) {
                            el.innerHTML = '<i class="far fa-check-circle green"></i>';
                        }
                        let dropDown = document.getElementById("moduleForSubject");
                        dropDown.selectedIndex = 0;
                    }
                }
                else{
                    this.setState({
                        'userMessage': "A error has been occurred",
                        'userStatus': 'negative'
                    })
                }
            })
    }

    insertSubject(){
        let element = document.getElementById('addSubject');
        element.classList.add('loading');
        EngineProjects.insertProjectElement(this.state.project_id,"subject", {"text": this.state.subject_new, "type": this.state.subject_new_type})
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                           'userMessage': res.msg,
                            'userStatus': "negative"
                        })
                    }
                    else if(res.status === "success"){
                        EngineProjects.selectProjectElement(this.state.project_id, "subject")
                            .then(res2 => {
                               this.setState({
                                   'project_subject': res2.results
                               })
                            });
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "positive"
                        })
                    }
                }
                else{
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': "A error has been occurred.",
                            'userStatus': "negative"
                        })
                    }
                }
                element.classList.remove('loading');
            })
    }

    loadModulesFromArray(modules){
        let rows = [];
        rows.push(
            <option key={0} value={""}>Please select module</option>
        );
        if(modules.length < 1){
            rows.push(
                <option key={1} value={""}>No module found for this subject.</option>
            );
            this.setState({'run_status': 'disabled'});
            return rows;
        }
        modules.forEach((module, i) => {
            rows.push(
                <option key={i+1} value={module.module_import}>{module.module_description}</option>
            )
        });
        return rows;
    }

    onChangeArgument(e){
        if(e.target.dataset.argument !== undefined){
            let argumentName = e.target.dataset.argument;
            let argumentValue = e.target.value;
            this.state.moduleArguments.forEach((argument, i) => {
                if(argument.name === argumentName){
                    argument.value = argumentValue;
                }
            });
        }
    }

    listArgument(){
        let rows = [];
        if(this.state.moduleArguments.length < 1){
            rows.push(
                <div className={"ui field"} key={0}>
                    <label>No argument yet.</label>
                </div>
            );
            return rows;
        }
        this.state.moduleArguments.forEach((argument, i) => {
            let requiredText = <span></span>;
            if(argument.required === "yes"){
                requiredText = <span className={"red"}>required</span>;
            }
            if(this.state.waiting_subject_type === argument.name){
                rows.push(<div className={"ui field"} key={i}>
                    <label>{argument.name} {requiredText}</label>
                    <input data-argument={argument.name} type={"text"} onChange={this.onChangeArgument} placeholder={argument.placeholder}
                           defaultValue={this.state.waiting_subject}/>
                </div>);
                argument.value = this.state.waiting_subject
            }
            else {
                rows.push(
                    <div className={"ui field"} key={i}>
                        <label>{argument.name} {requiredText}</label>
                        <input data-argument={argument.name} onChange={this.onChangeArgument} type={"text"} placeholder={argument.placeholder} defaultValue={argument.value}/>
                    </div>
                );
            }
        });
        return rows;
    }

    onModuleSelect(e){
        EngineProjects.selectProjectModule(e.target.value)
            .then(res => {
               if(res.status !== undefined){
                   if(res.status === "forbidden"){
                       this.setState({
                           'userMessage': res.msg,
                           'userStatus': 'negative'
                       })
                   }
                   else if(res.status === "success"){
                       this.setState({
                           'moduleArgumentsNb': res.module.module_argument.length,
                           'moduleArguments': res.module.module_argument,
                           'module_selected': res.module.module_import,
                           'waiting_module_icon': this.state.valid_check,
                           'run_status': '',
                       })
                   }
               }
               else{
                   this.setState({
                       'userMessage': "A error has been occurred",
                       'userStatus': 'negative'
                   })
               }
            });
    }

    listTasks(){
        let rows = [];
        this.state.project_tasks.forEach((task, i) => {
            if(task.status === "executed") {
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"positive center aligned"}><i className="far fa-smile"></i></td>
                        <td><Link to={"/project/view/" + this.state.project_id + "/" + task.task_id}><button className={"ui button basic buttonBasic mini fluid"}><i className="fas fa-search-plus"></i></button> </Link></td>
                    </tr>
                )
            }else if(task.status === "pending"){
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"warning center aligned"}><i className="fas fa-spinner fa-pulse"></i></td>
                        <td>Waiting...</td>
                    </tr>
                )
            }
            else if(task.status === "error"){
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"negative center aligned"}><i className="fas fa-times"></i></td>
                        <td>Error found</td>
                    </tr>
                )
            }
            else if(task.status === "empty"){
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"center aligned"}><i className={"far fa-meh orange_text"}></i> </td>
                        <td>Empty result</td>
                    </tr>
                )
            }
        });
        return rows;
    }

    onRunModule(){
        let argumentsParsed = {};
        if(this.state.moduleArguments.length > 0) {
            this.state.moduleArguments.forEach((argument, i) => {
                if (argument.required === "yes") {
                    if (argument.value === "") {
                        this.setState({
                            'userMessage': "Please do not leave empty required argument for this module.",
                            'userStatus': 'negative',
                        });
                        return false;
                    }
                }
                argumentsParsed[argument.name] = argument.value;
            });
        }
        EngineModules.moduleExecuteProject(this.state.module_selected, argumentsParsed, this.state.project_id, this.state.waiting_subject)
            .then(res => {
                if(res.task !== undefined){
                    let listing_task = this.state.project_tasks;
                    listing_task.unshift(res.task);
                    this.setState({
                        'project_tasks': listing_task
                    })
                }
            });
    }

    render(){
        return(
            <Screen>
                    <NavProject projectId={this.state.project_id}/>

                    <Message userMessage={this.state.userMessage} userStatus={this.state.userStatus}/>
                <div className={"ui grid " + this.state.displayed}>
                    <div className="six wide column sixcol3">
                        <div className={"ui form"}>
                            <div className={"field"}>
                                <input type={"text"} placeholder={"email, website, ip address ..."} onChange={this.setSubject} defaultValue={this.state.subject_new}/>
                            </div>
                            <div className={"field"}>
                                <select className={"ui fluid dropdown"} onChange={this.setSubjectType}>
                                    <option value="email">E-mail</option>
                                    <option value="person">Person</option>
                                    <option value="website">Website</option>
                                    <option value="enterprise">Enterprise</option>
                                    <option value="ip_address">IP Address</option>
                                    <option value="link">Link</option>
                                    <option value="username">Username</option>
                                    <option value="software">Software</option>
                                </select>
                            </div>
                            <div className={"field"}>
                                <button id={"addSubject"} className={"ui button orange fluid"} onClick={this.insertSubject}><i className="fas fa-plus"></i></button>
                            </div>
                        </div>

                        <div className={"subjectList"} id={"style1"}>
                            <table className="ui table noradius tablesubject">
                                <thead>
                                </thead>
                                <tbody>
                                {this.viewSubject()}
                                </tbody>
                            </table>
                        </div>
                    </div>


                    <div className="ten wide column tencol">
                        <table className="ui table noradius form">
                            <tbody>
                            <tr className={this.state.waiting_subject_status}>
                                <td className="collapsing">
                                    <i className={this.state.waiting_subject_icon}></i>
                                </td>
                                <td>{this.state.waiting_subject}</td>
                            </tr>
                            <tr className={this.state.waiting_module_status}>
                                <td><i className={this.state.waiting_module_icon}></i></td>
                                <td>{this.state.waiting_module}</td>
                            </tr>
                            </tbody>
                        </table>
                        <h2 className="ui header">
                            <div className="content">
                                <div className="sub header">Module arguments ({this.state.moduleArgumentsNb})</div>
                            </div>
                        </h2>
                        <div className={"ui form module_argument_div"}>
                            {this.listArgument()}
                        </div>
                        <div className={"ui divider"} />
                        <button onClick={this.onRunModule} className={"ui button orange fluid " + this.state.run_status}><i className="fas fa-play"></i></button>
                        <h2 className="ui header">
                            <div className="content">
                                <div className="sub header">Project tasks ({this.state.project_tasks.length})</div>
                            </div>
                        </h2>
                                <table className="ui very basic table">
                                    <thead>
                                    <tr>
                                        <th>Module</th>
                                        <th>Started by</th>
                                        <th>Subject</th>
                                        <th>Created_at</th>
                                        <th>Status</th>
                                        <th>View</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {this.listTasks()}
                                    </tbody>
                                </table>
                    </div>
                </div>
            </Screen>
        )
    }
}

export class ViewProjectSubjects extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            'project_id': props.match.params.projectId,
            'subjects' : [],
            'userMessage': '',
            'userStatus': '',
            'subject_new': '',
            'subject_new_type': '',
            'waiting_subject_type': '',
            'rows_list': [<tr><td>Please wait we load your subjects...</td></tr>]
        };

        this.listSubjects = this.listSubjects.bind(this);
        this.getSubject = this.getSubject.bind(this);
        this.removeSubject = this.removeSubject.bind(this);
        this.insertSubject = this.insertSubject.bind(this);
        this.setSubject = this.setSubject.bind(this);
        this.setSubjectType = this.setSubjectType.bind(this);
        this.getSubject();
    }

    getSubject(){
        EngineProjects.selectProjectElement(this.state.project_id, 'subject')
            .then(res => {
                this.setState({
                    'subjects': res.results
                })
            });
    }

    removeSubject(e){
        EngineProjects.removeProjectElement(this.state.project_id, 'subject', e.target.dataset.id)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'success'
                        });
                        this.getSubject()
                    }
                }
                else{
                    this.setState({
                        'userMessage': 'A error has occured',
                        'userStatus': 'negative'
                    })
                }
            })
    }

    insertSubject(){
        let element = document.getElementById('addSubject');
        element.classList.add('loading');
        EngineProjects.insertProjectElement(this.state.project_id,"subject", {"text": this.state.subject_new, "type": this.state.subject_new_type})
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "negative"
                        })
                    }
                    else if(res.status === "success"){
                        EngineProjects.selectProjectElement(this.state.project_id, "subject")
                            .then(res2 => {
                                this.setState({
                                    'project_subject': res2.results
                                })
                            });
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "positive"
                        })
                        this.getSubject()
                    }
                }
                else{
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': "A error has been occurred.",
                            'userStatus': "negative"
                        })
                    }
                }
                element.classList.remove('loading');
            })
    }

    listSubjects(){
        let rows = [];
        if(this.state.subjects.length > 0){
            this.state.subjects.forEach((subject, i) => {
                rows.push(
                    <tr key={i} id={"element_id_" + subject.element_id}>
                        <td>{subject.element_text.text}</td>
                        <td>{subject.element_text.type}</td>
                        <td className={"right aligned collapsing"}><button onClick={this.removeSubject} data-id={subject.element_id} className={"ui button basic red mini"}>delete</button> </td>
                    </tr>
                )
            })
        }
        return rows;
    }

    setSubject(e){
        this.setState({
            'subject_new': e.target.value
        })
    }

    setSubjectType(e){
        this.setState({
            'subject_new_type': e.target.value,
            'waiting_subject_type': e.target.value
        })
    }

    render(){
        return(
            <Screen>
                <NavProject projectId={this.state.project_id}/>
                <Message userMessage={this.state.userMessage} userStatus={this.state.userStatus}/>
                <div className={"ui grid " + this.state.displayed}>
                    <div className="six wide column sixcol3">
                        <div className={"ui form"}>
                            <div className={"field"}>
                                <input type={"text"} placeholder={"email, website, ip address ..."} onChange={this.setSubject} defaultValue={this.state.subject_new}/>
                            </div>
                            <div className={"field"}>
                                <select className={"ui fluid dropdown"} onChange={this.setSubjectType}>
                                    <option value="email">E-mail</option>
                                    <option value="person">Person</option>
                                    <option value="website">Website</option>
                                    <option value="enterprise">Enterprise</option>
                                    <option value="ip_address">IP Address</option>
                                    <option value="link">Link</option>
                                    <option value="username">Username</option>
                                    <option value="software">Software</option>
                                    <option value="Social">Social account</option>
                                </select>
                            </div>
                            <div className={"field"}>
                                <button id={"addSubject"} className={"ui button orange fluid"} onClick={this.insertSubject}><i className="fas fa-plus"></i></button>
                            </div>
                        </div>
                    </div>
                    <div className="ten wide column tencol tencolmaxheight" id={"style1"}>
                        <table className="ui very basic table">
                            <thead>
                            </thead>
                            <tbody>
                            {this.listSubjects()}
                            </tbody>
                        </table>
                    </div>
                </div>
            </Screen>
        )
    }
}

export class ViewProjectThree extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            'project_id': props.match.params.projectId,
            'project_data': [
                {
                    'name': "Wait we load your project...",
                }
            ],
            'subject_selected': 'Please select a subject',
            'waiting_subject_type': '',
            'waiting_subject_icon': 'fas fa-ellipsis-h',
            'module_lists': [<select className={"ui dropdown"}><option>Please select a subject</option></select>],
            'moduleArgumentsNb': '0',
            'moduleArguments': [],
            'task': [],
            'task_results': [],
            'task_results_nb': '0',
            'module_selected': '',
            'selected_task': '',
            'run_status': 'disabled',
            'project_tasks': []
        };

        EngineProjects.loadProjectsThree(props.match.params.projectId)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'project_data': [res.three],
                            'project_id': props.match.params.projectId,
                            'project_tasks': res.tasks,
                        })
                    }
                }
                else{
                    this.setState({
                        'userMessage': "A error as occurred",
                        'userStatus': 'negative'
                    })
                }
            });
        this.onNodeClick = this.onNodeClick.bind(this);
        this.loadModulesFromArray = this.loadModulesFromArray.bind(this);
        this.onModuleSelect = this.onModuleSelect.bind(this);
        this.listArgument = this.listArgument.bind(this);
        this.onRunModule = this.onRunModule.bind(this);
        this.listTasks = this.listTasks.bind(this);
        this.loadTasks = this.loadTasks.bind(this);
        this.loadTaskUnique = this.loadTaskUnique.bind(this);
        this.getHeaders = this.getHeaders.bind(this);
        this.getResults = this.getResults.bind(this);
    }

    componentDidMount() {
        const dimensions = this.treeContainer.getBoundingClientRect();
        this.counter = setInterval(
            () => this.loadTasks(),
            10000
        );
        this.setState({
            translate: {
                x: dimensions.width / 2,
                y: 30
            }
        });
    }

    componentWillUnmount() {
        clearInterval(this.counter);
    }

    listArgument(){
        let rows = [];
        if(this.state.moduleArguments.length < 1){
            rows.push(
                <div className={"ui field"} key={0}>
                    <label>No argument yet.</label>
                </div>
            );
            return rows;
        }
        this.state.moduleArguments.forEach((argument, i) => {
            let requiredText = <span></span>;
            if(argument.required === "yes"){
                requiredText = <span className={"red"}>required</span>;
            }
            if(this.state.waiting_subject_type === argument.name){
                rows.push(<div className={"ui field"} key={i}>
                    <label>{argument.name} {requiredText}</label>
                    <input data-argument={argument.name} type={"text"} onChange={this.onChangeArgument} placeholder={argument.placeholder}
                           defaultValue={this.state.subject_selected}/>
                </div>);
                argument.value = this.state.subject_selected
            }
            else {
                rows.push(
                    <div className={"ui field"} key={i}>
                        <label>{argument.name} {requiredText}</label>
                        <input data-argument={argument.name} onChange={this.onChangeArgument} type={"text"} placeholder={argument.placeholder} defaultValue={argument.value}/>
                    </div>
                );
            }
        });
        return rows;
    }

    onModuleSelect(e){
        EngineProjects.selectProjectModule(e.target.value)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'moduleArgumentsNb': res.module.module_argument.length,
                            'moduleArguments': res.module.module_argument,
                            'module_selected': res.module.module_import,
                            'run_status': '',
                        })
                    }
                }
                else{
                    this.setState({
                        'userMessage': "A error has been occurred",
                        'userStatus': 'negative'
                    })
                }
            });
    }

    loadModulesFromArray(modules){
        let rows = [];
        rows.push(
            <option key={0} value={""}>Please select module</option>
        );
        if(modules.length < 1){
            rows.push(
                <option key={1} value={""}>No module found for this subject.</option>
            );
            return rows;
        }
        modules.forEach((module, i) => {
            rows.push(
                <option key={i+1} value={module.module_import}>{module.module_description}</option>
            )
        });
        return rows;
    }

    listTasks(){
        let rows = [];
        this.state.project_tasks.forEach((task, i) => {
            if(task.status === "executed") {
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"positive center aligned"}><i className="far fa-smile"></i></td>
                        <td><Link to={"/project/view/" + this.state.project_id + "/" + task.task_id}><button className={"ui button basic buttonBasic mini fluid"}><i className="fas fa-search-plus"></i></button> </Link></td>
                    </tr>
                )
            }else if(task.status === "pending"){
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"warning center aligned"}><i className="fas fa-spinner fa-pulse"></i></td>
                        <td>Waiting...</td>
                    </tr>
                )
            }
            else if(task.status === "error"){
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"negative center aligned"}><i className="fas fa-times"></i></td>
                        <td>Error found</td>
                    </tr>
                )
            }
            else if(task.status === "empty"){
                rows.push(
                    <tr key={i}>
                        <td>{task.module_name}</td>
                        <td>{task.username}</td>
                        <td>{task.project_subject}</td>
                        <td>{task.created_at}</td>
                        <td className={"center aligned"}><i className={"far fa-meh orange_text"}></i> </td>
                        <td>Empty result</td>
                    </tr>
                )
            }
        });
        return rows;
    }

    loadTasks(){
        clearInterval(this.counter);
        EngineProjects.getProjectTask(this.state.project_id)
            .then(res => {
                if(res.status === "success" && res.tasks !== undefined){
                    this.setState({
                        'project_tasks': res.tasks,
                    })
                }
                this.counter = setInterval(
                    () => this.loadTasks(),
                    10000
                );
            })
    }

    onRunModule(){
        let argumentsParsed = {};
        if(this.state.moduleArguments.length > 0) {
            this.state.moduleArguments.forEach((argument, i) => {
                if (argument.required === "yes") {
                    if (argument.value === "") {
                        this.setState({
                            'userMessage': "Please do not leave empty required argument for this module.",
                            'userStatus': 'negative',
                        });
                        return false;
                    }
                }
                argumentsParsed[argument.name] = argument.value;
            });
        }
        EngineModules.moduleExecuteProject(this.state.module_selected, argumentsParsed, this.state.project_id, this.state.subject_selected)
            .then(res => {
                if(res.task !== undefined){
                    let listing_task = this.state.project_tasks;
                    listing_task.unshift(res.task);
                    this.setState({
                        'project_tasks': listing_task
                    })
                }
            });
    }

    onNodeClick(node){
        if(node.element_id !== undefined){
            EngineProjects.selectProjectThemes(this.state.project_id, node.element_id)
                .then(res => {
                    if(res.status !== undefined){
                        if(res.status === "forbidden"){
                            this.setState({
                                'userMessage': res.msg,
                                'userStatus': 'negative'
                            })
                        }
                        else if(res.status === "success"){
                            this.setState({
                                'subject_selected': node.name,
                                'waiting_subject_type': node.attributes.type,
                                'waiting_subject_icon': 'far fa-check-circle green',
                                'module_lists': <select id={"moduleForSubject"} onChange={this.onModuleSelect} className={"ui dropdown"}>{this.loadModulesFromArray(res.modules)}</select>,
                                'moduleArgumentsNb': '0',
                                'run_status': 'disabled',
                                'moduleArguments': [],
                            });
                            let dropDown = document.getElementById("moduleForSubject");
                            dropDown.selectedIndex = 0;
                        }
                    }
                    else{
                        this.setState({
                            'userMessage': "A error has been occurred",
                            'userStatus': 'negative'
                        })
                    }
                })
        }
    }

    loadTaskUnique(task_id){
        EngineProjects.getProjectTaskUnique(this.state.project_id, task_id)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        let result_task = [];
                        if(res.task.results[0] !== undefined){
                            result_task = res.task.results[0]
                        }
                        this.setState({
                            'task': res.task,
                            'task_results': result_task,
                            'task_results_nb': result_task.length
                        })
                    }
                }
                else{
                    this.setState({
                        'userMessage': "A error has ben occurred",
                        'userStatus': 'negative'
                    })
                }
            });
    }

    getHeaders(){
        let rows = [];
        let headers_list = [];

        this.state.task_results.forEach((result, index) => {
            if(Object.keys(result).length > 0){
                Object.keys(result).forEach((header, index2) => {
                    if(headers_list.indexOf(header) <= -1){
                        headers_list.push(header);
                    }
                })
            }
        });
        if(headers_list.length > 0){
            headers_list.forEach((header, i) => {
                rows.push(<th key={i}>{header}</th>)
            });
        }
        return rows;
    }

    getResults(){
        let rows = [];
        this.state.task_results.forEach((result, index) => {
            let result_tpl = [];
            if(Object.keys(result).length > 0) {
                Object.keys(result).forEach((header, i) => {
                    result_tpl.push(
                        <td onClick={this.setDataSet} data-value={result[header]} key={i}>{result[header]}</td>
                    )
                });
            }
            rows.push(<tr key={index}>{result_tpl}</tr>)
        });
        return rows;
    }

    render(){
        return(
            <Screen>
                <NavProject projectId={this.state.project_id}/>
                <div className={"ui grid " + this.state.displayed}>
                    <div className="four wide column sixcol5">

                        <div className={"ui form"}>
                            <div className={"field"}>
                                <label>Subject</label>
                                <table className="ui table noradius form">
                                    <tbody>
                                    <tr className="" key={0}>
                                        <td className="collapsing">
                                            <i className={this.state.waiting_subject_icon}></i>
                                        </td>
                                        <td>{this.state.subject_selected}</td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div className={"field"}>
                                <label>Select a module</label>
                                {this.state.module_lists}
                            </div>
                            <h2 className="ui header">
                                <div className="content">
                                    <div className="sub header">Module arguments ({this.state.moduleArgumentsNb})</div>
                                </div>
                            </h2>
                            <div className={"ui form module_argument_div"}>
                                {this.listArgument()}
                            </div>
                            <div className={"ui divider"} />
                            <button onClick={this.onRunModule} className={"ui button orange fluid " + this.state.run_status}><i className="fas fa-play"></i></button>

                        </div>
                    </div>
                    <div className="twelve wide column tencol2">
                        <div id="treeWrapper" style={containerStyles} ref={tc => (this.treeContainer = tc)}>

                            <Tree onClick={this.onNodeClick} collapsible={false} translate={this.state.translate} nodeSize={{x: 200, y: 200}} data={this.state.project_data} orientation={"vertical"} />

                        </div>
                    </div>
                </div>
                <div className={"taskcol"}>
                    <h4 className={"ui header"}>Project history</h4>
                    <table className="ui very basic table">
                        <thead>
                        </thead>
                        <tbody>
                        {this.listTasks()}
                        </tbody>
                    </table>
                </div>
            </Screen>
        )
    }
}

export class ViewProjectTask extends React.Component{
    constructor(props){

        super(props);
        this.state = {
            'userMessage': 'Please wait, we open a task...',
            'userStatus': 'warning',
            'project_id': props.match.params.projectId,
            'displayed': '',
            'headers': [],
            'project_info': [],
            'task': [],
            'task_results': [],
            'task_results_nb': '0',
            'project_subject': [],
            'subject_new': '',
            'note_text': '',
            'subject_new_type':'email',
            'waiting_subject_type':'',
            'task_information': {},
            'group_by': ''
        };

        EngineProjects.loadProjects(props.match.params.projectId)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'userMessage': '',
                            'userStatus': '',
                            'project_info': res.projects,
                            'project_subject': res.subjects,
                            'project_id': props.match.params.projectId
                        })
                    }
                }
            });

        EngineProjects.getProjectTaskUnique(props.match.params.projectId, props.match.params.taskId)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        let result_task = [];
                        if(res.task.results[0] !== undefined){
                            result_task = res.task.results[0]
                        }
                        this.setState({
                            'task': res.task,
                            'task_results': result_task,
                            'task_results_nb': result_task.length,
                            'group_by': res.task.group_by
                        })
                    }
                }
                else{
                    this.setState({
                        'userMessage': "A error has ben occurred",
                        'userStatus': 'negative'
                    })
                }
            });

        this.insertSubject = this.insertSubject.bind(this);
        this.viewSubject = this.viewSubject.bind(this);
        this.setSubject = this.setSubject.bind(this);
        this.setSubjectType = this.setSubjectType.bind(this);
        this.getResults = this.getResults.bind(this);
        this.getHeaders = this.getHeaders.bind(this);
        this.setDataSet = this.setDataSet.bind(this);
        this.getSubject = this.getSubject.bind(this);
        this.noteChange = this.noteChange.bind(this);
        this.insertNote = this.insertNote.bind(this);
        this.moduleOutput = this.moduleOutput.bind(this);
        this.onSelectTxt = this.onSelectTxt.bind(this);
        this.setGroupBy = this.setGroupBy.bind(this);
    }

    insertSubject(){
        let element = document.getElementById('addSubject');
        element.classList.add('loading');
        EngineProjects.insertProjectElementFrom(this.state.project_id,"subject", {"text": this.state.subject_new, "type": this.state.subject_new_type}, this.state.task.project_subject, this.state.group_by)
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "negative"
                        })
                    }
                    else if(res.status === "success"){
                        EngineProjects.selectProjectElement(this.state.project_id, "subject")
                            .then(res2 => {
                                this.setState({
                                    'userMessage': "",
                                    'userStatus': "",
                                    'project_subject': res2.results
                                })
                            });
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "positive"
                        })
                    }
                }
                else{
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': "A error has been occurred.",
                            'userStatus': "negative"
                        })
                    }
                }
                element.classList.remove('loading');
            })
    }

    componentDidMount() {
        this.deleteAlert = setInterval(
            () => {
                if(this.state.userStatus !== '' || this.state.userMessage !== '') {
                    this.setState({
                        'userMessage': '',
                        'userStatus': ''
                    })
                }
            }, 10000
        )
    }

    componentWillUnmount() {
        clearInterval(this.deleteAlert)
    }

    insertNote(){
        let element = document.getElementById('addNote');
        element.classList.add('loading');
        EngineProjects.insertProjectElement(this.state.project_id,"note", {"subject": this.state.subject_new, "subject_type": this.state.subject_new_type, "note_text": this.state.note_text, "task_id": this.state.task.task_id}, "")
            .then(res => {
                if(res.status !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "negative"
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': "positive"
                        })
                    }
                }
                else{
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': "A error has been occurred.",
                            'userStatus': "negative"
                        })
                    }
                }
                element.classList.remove('loading');
            })
    }

    getSubject(){
        return this.state.subject_new
    }

    viewSubject(){
        let rows = [];
        this.state.project_subject.forEach((element, i) => {
            rows.push(
                <tr key={i}>
                    <td>{element.element_text.text} <small>({element.element_text.type})</small></td>
                </tr>
            )
        });
        return rows
    }

    setSubject(e){
        this.setState({
            'subject_new': e.target.value
        })
    }

    setSubjectType(e){
        this.setState({
            'subject_new_type': e.target.value,
            'waiting_subject_type': e.target.value
        })
    }

    getHeaders(){
        let rows = [];
        let headers_list = [];
        let cmp = 0;

        this.state.task_results.forEach((result, index) => {
            if(Object.keys(result).length > 0){
                Object.keys(result).forEach((header, index2) => {
                    if(headers_list.indexOf(header) <= -1){
                        headers_list.push(header);
                    }
                })
            }
        });
        if(headers_list.length > 0){
            headers_list.forEach((header, i) => {
               rows.push(<th key={i}>{header}</th>)
                cmp = i;
            });
        }
        rows.push(<th key={cmp}></th>);
        return rows;
    }

    setDataSet(e){
        this.setState({
            'subject_new': e.target.dataset.value
        })
    }

    setGroupBy(e){
        console.log(e.target.value)
        this.setState({
            'group_by': e.target.value
        })
    }

    onSelectTxt(){
        let txt = "";
        if (window.getSelection) {
            txt = window.getSelection();
        }
        else if (document.getSelection) {
            txt = document.getSelection();
        } else if (document.selection) {
            txt = document.selection.createRange().text;
        }
        else{
            return false;
        }

        this.setState({
            'subject_new': txt
        })
    }

    moduleOutput(){
        let module_output = this.state.task.module_output;
        if(module_output === "rows") {
            return (

                <table className="ui table">
                    <thead>
                    <tr>
                        {this.getHeaders()}
                    </tr>
                    </thead>
                    <tbody>
                    {this.getResults()}
                    </tbody>
                </table>
            )
        }
        else if(module_output === "textarea"){
            return (
                <pre onMouseUp={this.onSelectTxt}>
                    {this.state.task.results}
                </pre>
            )
        }
        else{
            return (
                <p>Output module unknown</p>
            )
        }

    }

    noteChange(e){
        this.setState({
            'note_text': e.target.value
        })
    }

    getResults(){
        let rows = [];
        this.state.task_results.forEach((result, index) => {
            let result_tpl = [];
            if(Object.keys(result).length > 0) {
                Object.keys(result).forEach((header, i) => {
                    result_tpl.push(
                        <td onClick={this.setDataSet} data-value={result[header]} key={i}>{result[header]}</td>
                    )
                });
                result_tpl.push(<td><button className={"ui button basic mini buttonBasic"}><i className="fas fa-flag red"></i></button> </td>)

            }
            rows.push(<tr key={index}>{result_tpl}</tr>)
        });
        return rows;
    }

    render(){
        const subjectNew = this.state.subject_new;
        const noteText = this.state.note_text;
        return(
            <Screen>
                <Message userMessage={this.state.userMessage} userStatus={this.state.userStatus}/>
                <NavProject projectId={this.state.project_id}/>
                <div className={"ui grid " + this.state.displayed}>
                    <div className="six wide column sixcol3">
                        <h4 className="ui header">
                            <div className="content">
                                Task informations
                            </div>
                        </h4>
                            <table className="ui table noradius form">
                                <tbody>
                                <tr className="">
                                    <td className="collapsing">
                                       Module
                                    </td>
                                    <td>
                                        <b>{this.state.task.module_name}</b>
                                    </td>
                                </tr>
                                <tr className="">
                                    <td className="collapsing">
                                        Subject
                                    </td>
                                    <td>
                                        <b>{this.state.task.project_subject}</b>
                                    </td>
                                </tr>
                                <tr className="">
                                    <td className="collapsing">
                                        Task id
                                    </td>
                                    <td>
                                        <b>{this.state.task.task_id}</b>
                                    </td>
                                </tr>
                                <tr className="">
                                    <td className="collapsing">
                                        Results
                                    </td>
                                    <td>
                                        <b>{this.state.task_results_nb}</b>
                                    </td>
                                </tr>
                                </tbody>
                            </table>
                        <h4 className="ui header">
                            <div className="content">
                                Click on result for interact
                            </div>
                        </h4>
                        <div className={"sixcol2"}>
                        <div className={"ui form"}>
                            <div className={"field"}>
                                <input type={"text"} placeholder={"email, website, ip address ..."} onChange={this.setSubject} value={subjectNew}/>
                            </div>
                            <div className={"field"}>
                                <select className={"ui fluid dropdown"} onChange={this.setSubjectType}>
                                    <option value="email">E-mail</option>
                                    <option value="person">Person</option>
                                    <option value="website">Website</option>
                                    <option value="enterprise">Enterprise</option>
                                    <option value="ip_address">IP Address</option>
                                    <option value="link">Link</option>
                                    <option value="username">Username</option>
                                    <option value="software">Software</option>
                                    <option value="Exploit_CVE">Exploit - CVE</option>
                                    <option value="social">Social account</option>
                                    <option value="result">Result</option>
                                    <option value="Port">Port</option>
                                </select>
                            </div>
                            <div className={"field"}>
                                <label>Graphical grouping</label>
                                <input type={"text"} placeholder={"software, headers, subdomains..."} onChange={this.setGroupBy} defaultValue={this.state.group_by}/>
                            </div>
                            <div className={"field"}>
                                <textarea onChange={this.noteChange}>{noteText}</textarea>
                            </div>
                            <div className={"two fields"}>
                                <div className={"field"}>
                                    <button id={"addSubject"} className={"ui button basic buttonBasic fluid"} onClick={this.insertSubject}>Add Suject <i className="fas fa-plus"></i></button>
                                </div>
                                <div className={"field"}>
                                    <button id={"addNote"} className={"ui button basic buttonBasic fluid"} onClick={this.insertNote}>Add Note <i className="fas fa-plus"></i></button>
                                </div>
                            </div>
                        </div>
                        </div>
                    </div>
                    <div className="ten wide column tencol tencolmaxheight" id={"style1"}>
                        {this.moduleOutput()}
                    </div>
                </div>
            </Screen>
        )
    }
}

export class ExportProjectJson extends React.Component{
    constructor(props){
        super(props);
        console.log(props);
        this.state = {
            'json_export': {
                "status": "we convert your project to json please wait."
            },
            'project_id': props.match.params.projectId
        };
        EngineProjects.exportProjectJson(props.match.params.projectId)
            .then(res => {
                if(res.status === undefined){
                    if(res.project !== undefined){
                        this.setState({
                            'json_export': res
                        })
                    }
                }
            })
    }

    render() {
        return (
            <Screen>
                <NavProject projectId={this.state.project_id}/>
                <Highlight className='json preHight' id={"style1"}>
                    {JSON.stringify(this.state.json_export, undefined, 2)}
                </Highlight>
            </Screen>
        )
    }
}

export class ExportProjectXml extends React.Component{
    constructor(props){
        super(props);
        console.log(props);
        this.state = {
            'xml_export': "<root>\n     <project>\n         <message>Please wait we convert your project to XML</message>\n      </project>\n</root>",
            'project_id': props.match.params.projectId
        };
        EngineProjects.exportProjectXml(props.match.params.projectId)
            .then(res => {
                if(res.status === undefined){
                    if(res.export !== undefined){
                        this.setState({
                            'xml_export': res.export
                        })
                    }
                }
            })
    }

    render() {
        return (
            <Screen>
                <NavProject projectId={this.state.project_id}/>
                <Highlight className='HTML preHight' id={"style1"}>
                    {this.state.xml_export}
                </Highlight>
            </Screen>
        )
    }
}

export default Projects