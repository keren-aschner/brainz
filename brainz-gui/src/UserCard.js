import React from 'react';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';


class UserCard extends React.Component {
    render() {
        return (
            <div>
                <Card style={{width: '18rem'}}>
                    <Card.Body>
                        <Card.Title>User {this.props.id}</Card.Title>
                        <Card.Text>
                            User data
                        </Card.Text>
                        <Button onClick={this.props.onClick}>See Snapshots</Button>
                    </Card.Body>
                </Card>
            </div>
        );
    }
}

export default UserCard;
