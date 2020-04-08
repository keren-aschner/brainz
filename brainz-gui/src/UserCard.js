import React from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';


class UserCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {user: {}}
    }

    componentDidMount() {
        fetch("/users/" + this.props.user_id)
            .then(response => response.json())
            .then(data => this.setState({user: data}));
    }

    render() {
        let user = this.state.user;

        return (
            <div>
                <Card style={{width: '18rem'}}>
                    <Card.Body>
                        <Card.Title>{user.username}</Card.Title>
                        <Card.Text>
                            ID: {user.user_id}<br/>
                            Birthday: {new Date(user.birthday * 1000).toDateString()}<br/>
                            Gender: {user.gender === 'f' ? 'Female' : 'Male'}
                        </Card.Text>
                        <Button onClick={this.props.onClick}>See Snapshots</Button>
                    </Card.Body>
                </Card>
            </div>
        );
    }
}

export default UserCard;
