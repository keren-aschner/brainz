import React from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';


class UserCard extends React.Component {
    render() {
        let user;
        if (this.props.user_id === 1) {
            user = {user_id: 1, username: "Keren Solodkin", birthday: 856828800.0, gender: 'f'};
        } else {
            user = {user_id: 2, username: "Bar Aschner", birthday: 864259200.0, gender: 'm'};
        }

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
