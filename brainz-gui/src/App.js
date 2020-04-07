import React from 'react';
import logo from './brainz.png';
import Navbar from 'react-bootstrap/Navbar';
import UserCard from "./UserCard";
import CardDeck from 'react-bootstrap/CardDeck'
import User from "./User";

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {user: null};
    }

    viewUser(userId) {
        this.setState({user: userId});
    }

    render() {
        const users = [{id: 1, name: "Keren"}, {id: 2, name: "Bar"}];
        let pageData;
        if (this.state.user == null) {
            pageData =
                <CardDeck>
                    {users.map((user) =>
                        <UserCard key={user.id} id={user.id} onClick={this.viewUser.bind(this, user.id)}/>)}
                </CardDeck>;
        } else {
            pageData = <User id={this.state.user}/>
        }
        return (
            <div>
                <Navbar bg="light">
                    <Navbar.Brand onClick={this.viewUser.bind(this, null)}>
                        <img alt="" src={logo} width="50" height="47" className="d-inline-block align-top"/>{' '}
                        Brainz
                    </Navbar.Brand>
                </Navbar>
                {pageData}
            </div>
        );
    }
}

export default App;
