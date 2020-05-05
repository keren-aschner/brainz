import React from 'react';
import {Button, Card} from 'antd'
import {CameraOutlined} from '@ant-design/icons'

class UserCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {user: {}}
    }

    componentDidMount() {
        fetch(`${window.api_server}/users/${this.props.user_id}`)
            .then(response => response.json())
            .then(data => this.setState({user: data}));
    }

    render() {
        let user = this.state.user;

        return (
            <div>
                <Card style={{margin: 40, width: 300, background: '#fafafa'}} title={user.username} actions={[
                    <Button type="link" onClick={this.props.onClick}><CameraOutlined/>snapshots</Button>
                ]}>
                    <p>ID: {user.user_id}</p>
                    <p>Birthday: {new Date(user.birthday * 1000).toDateString()}</p>
                    <p>Gender: {user.gender === 'f' ? 'Female' : 'Male'}</p>
                </Card>
            </div>
        );
    }
}

export default UserCard;
