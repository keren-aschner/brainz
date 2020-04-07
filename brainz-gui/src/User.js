import React from 'react';
import Alert from 'react-bootstrap/Alert'

class UserCard extends React.Component {
    render() {
        return (
            <div>
                <Alert>
                    User {this.props.id}
                </Alert>
            </div>
        );
    }
}

export default UserCard;
