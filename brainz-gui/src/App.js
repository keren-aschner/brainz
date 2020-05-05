import React from 'react';
import logo from './brainz.png';
import UserCard from "./UserCard";
import CardDeck from 'react-bootstrap/CardDeck'
import User from "./User";
import {Menu} from 'antd'

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {user: null, users: []};
    }

    componentDidMount() {
        fetch(`${window.api_server}/users`)
            .then(response => response.json())
            .then(data => this.setState({users: data}));
    }

    viewUser(userId) {
        this.setState({user: userId});
    }

    render() {
        let users = this.state.users;
        let pageData;
        if (this.state.user == null) {
            pageData =
                <CardDeck>
                    {users.map((user) =>
                        <UserCard key={user.user_id} user_id={user.user_id}
                                  onClick={this.viewUser.bind(this, user.user_id)}/>)}
                </CardDeck>;
        } else {
            pageData = <User user_id={this.state.user}/>
        }
        return (
            <div>
                <Menu style={{height: 75, background: '#fafafa'}} selectedKeys={[]} mode="horizontal">
                    <Menu.Item disabled>
                        <img alt="" src={logo} height="60"/>{' '}
                    </Menu.Item>
                    <Menu.Item onClick={this.viewUser.bind(this, null)}>
                        <div style={{fontSize: 30, color: '#273B92'}}>Brainz</div>
                    </Menu.Item>
                    <Menu.SubMenu title='Users'>
                        {users.map((user) =>
                            <Menu.Item key={user.user_id} onClick={this.viewUser.bind(this, user.user_id)}>
                                {user.username}
                            </Menu.Item>)}
                    </Menu.SubMenu>
                </Menu>
                {pageData}
            </div>
        );
    }
}

export default App;
