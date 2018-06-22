import React from "react";
import {NavProject} from '../Nav'
import Message from '../Message'
import EngineProjects from '../Database/Engine/Projects'
import EngineBreach from '../Database/Engine/Breach'
import styled from 'styled-components'

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

class ViewBreach extends React.Component{

    constructor(props){
        super(props);
        this.state = {
            'project_id': props.match.params.projectId,
            'subjects' : [],
            'userMessage': '',
            'userStatus': '',
            'subject_new': '',
            'subject_new_type': 'email',
            'waiting_subject_type': '',
            'search_text': '',
            'search_type': 'email',
            'available_search': [<option key={0}>No element available in database.</option>],
            'results_amount': 0,
            'results_data': []
        };

        this.listSubjects = this.listSubjects.bind(this);
        this.getSubject = this.getSubject.bind(this);
        this.insertSubject = this.insertSubject.bind(this);
        this.setSubject = this.setSubject.bind(this);
        this.setSubjectType = this.setSubjectType.bind(this);
        this.pushSearch = this.pushSearch.bind(this);
        this.pushText = this.pushText.bind(this);
        this.pushType = this.pushType.bind(this);
        this.searchOutput = this.searchOutput.bind(this);
        this.getHeaders = this.getHeaders.bind(this);
        this.getResults = this.getResults.bind(this);
        this.setDataSet = this.setDataSet.bind(this);
        this.setSubjectType = this.setSubjectType.bind(this);
        this.getSubject();

        EngineBreach.breachInformation()
            .then(res => {
                if(res.status === 'forbidden'){
                    this.setState({
                        'userStatus': 'negative',
                        'userMessage': res.msg
                    })
                }
                else if(res.status === "success"){
                    let available_search = [];
                    if(res.searchables.length > 0){
                        res.searchables.forEach((value, index) => {
                            available_search.push(
                                <option key={index} value={value}>{value}</option>
                            )
                        })
                    }
                    else{
                        available_search.push(
                                <option key={0} value="">No element available in database.</option>
                            )
                    }
                    this.setState({
                        'available_search': available_search,
                        'results_amount': res.results
                    })
                }
                else{
                    this.setState({
                        'userStatus': 'negative',
                        'userMessage': 'Error has occured.'
                    })
                }
            })
    }

    pushType(e){
        this.setState({
            'search_type': e.target.value
        })
    }

    pushText(e){
        this.setState({
            'search_text': e.target.value
        })
    }

    setSubjectType(e){
        this.setState({
            'subject_new_type': e.target.value,
            'waiting_subject_type': e.target.value
        })
    }

    setDataSet(e){
        this.setState({
            'subject_new': e.target.dataset.value
        })
    }

    getHeaders(){
        let rows = [];
        let headers_list = [];

        this.state.results_data.forEach((result, index) => {
            if(result.length > 0){
                result.forEach((r2, _) => {
                    Object.keys(r2).forEach((header, _) => {
                        if(headers_list.indexOf(header) <= -1){
                            headers_list.push(header);
                        }
                    })
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
        this.state.results_data.forEach((result, index) => {
            if(result.length > 0){
                let result_tpl = [];
                let index_v = 0
                result.forEach((r2, i2) => {
                   if(Object.keys(r2).length > 0) {
                        Object.keys(r2).forEach((header, i) => {
                            index_v = (i * i2)
                            result_tpl.push(
                                <td onClick={this.setDataSet} data-value={r2[header]} key={i2+i}>{r2[header]}</td>
                            )
                        });

                    }
                });
                rows.push(<tr key={index_v}>{result_tpl}</tr>)
            }
        });
        return rows;
    }

    searchOutput(){
        return (

                <table className="ui table">
                    <thead>
                    {this.getHeaders()}
                    </thead>
                    <tbody>
                    {this.getResults()}
                    </tbody>
                </table>
            )
    }

    pushSearch(){
        if(this.state.search_text !== '' && this.state.search_type !== ''){
            EngineBreach.breachSearch(this.state.search_text, this.state.search_type)
                .then(res => {
                    if(res.status === 'forbidden'){
                    this.setState({
                        'userStatus': 'negative',
                        'userMessage': res.msg
                    })
                }
                else if(res.status === "success"){
                        console.log(res);
                        this.setState({
                            'results_data': res.results
                        })
                }
                else{
                    this.setState({
                        'userStatus': 'negative',
                        'userMessage': 'Error has occured.'
                    })
                }
                })
        }
        else{
            this.setState({
                'userMessage': 'Please enter text and type',
                'userStatus': 'negative'
            })
        }
    }

    getSubject(){
        EngineProjects.selectProjectElement(this.state.project_id, 'subject')
            .then(res => {
                this.setState({
                    'subjects': res.results
                })
            });
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
                        <div className={"ui form"}>
                            <div className={"field"}>
                                <label>Search in database ({this.state.results_amount} results avaiable)</label>
                                <input onChange={this.pushText} type={"text"} placeholder={"ex: Jhon@doe.com"} />
                            </div>
                            <div className={"field"}>
                                 <select className={"ui fluid dropdown"} onChange={this.pushType}>
                                     {this.state.available_search}
                                 </select>
                            </div>
                             <div className={"field"}>
                                 <button onClick={this.pushSearch} className={"ui button basic fluid buttonBasic"}>search now</button>
                            </div>
                        </div>
                        {this.searchOutput()}
                    </div>
                </div>
            </Screen>
        )
    }
}

export default ViewBreach;