import React from 'react';
import CanvasJSReact from "./canvasjs/canvasjs.react";
import Button from "react-bootstrap/Button";

var CanvasJSChart = CanvasJSReact.CanvasJSChart;


class UserCard extends React.Component {
    constructor(props) {
        super(props);
        this.changeTimestamp = this.changeTimestamp.bind(this);
        this.playImages = this.playImages.bind(this);
        this.state = {snapshot: null, snapshot_id: null, playing: false, feelings: [], snapshots: []};
    }

    componentDidMount() {
        fetch("/users/" + this.props.user_id + "/feelings")
            .then(response => response.json())
            .then(data => this.setState({feelings: data}));
    }

    changeTimestamp(e) {
        if (!this.state.playing) {
            this.setState({snapshot_id: e.dataPoint.id});
        }
    }

    playImages(e) {
        fetch("/users/" + this.props.user_id + "/snapshots")
            .then(response => response.json())
            .then(data => this.setState({snapshots: data}));

        this.setState({
            snapshot: 0,
            playing: true
        });
        this.timerID = setInterval(
            () => this.tick(),
            250
        );
    }

    tick() {
        let snapshotsSize = this.state.snapshots.length - 1;
        if (this.state.snapshot === snapshotsSize) {
            clearInterval(this.timerID);
            this.setState({playing: false});
            return;
        }

        this.setState(state => ({
            snapshot: state.snapshot + 1,
        }));
        this.setState(state => ({
            snapshot_id: state.snapshots[state.snapshot].snapshot_id
        }));
    }

    render() {
        let feelings = this.state.feelings;

        const feelingsOptions = {
            theme: "light2",
            animationEnabled: true,
            title: {
                text: "Feelings over time"
            },
            axisY: {
                title: "Feelings",
            },
            axisX: {
                title: "timestamp",
                valueFormatString: "D MMM HH:mm:ss.f",
            },
            toolTip: {
                shared: true
            },
            data: [
                {
                    type: "spline",
                    name: "hunger",
                    mousemove: this.changeTimestamp,
                    xValueFormatString: "DD.MM.YY HH:mm:ss.fff",
                    showInLegend: true,
                    dataPoints: feelings.map((snapshot) => {
                            return {
                                id: snapshot.snapshot_id,
                                x: new Date(snapshot.timestamp * 1000),
                                y: snapshot.feelings.hunger
                            }
                        }
                    )
                },
                {
                    type: "spline",
                    name: "thirst",
                    mousemove: this.changeTimestamp,
                    xValueFormatString: "DD.MM.YY HH:mm:ss.fff",
                    showInLegend: true,
                    dataPoints: feelings.map((snapshot) => {
                            return {
                                id: snapshot.snapshot_id,
                                x: new Date(snapshot.timestamp * 1000),
                                y: snapshot.feelings.thirst
                            }
                        }
                    )
                },
                {
                    type: "spline",
                    name: "exhaustion",
                    mousemove: this.changeTimestamp,
                    xValueFormatString: "DD.MM.YY HH:mm:ss.fff",
                    showInLegend: true,
                    dataPoints: feelings.map((snapshot) => {
                            return {
                                id: snapshot.snapshot_id,
                                x: new Date(snapshot.timestamp * 1000),
                                y: snapshot.feelings.exhaustion
                            }
                        }
                    )
                },
                {
                    type: "spline",
                    name: "happiness",
                    mousemove: this.changeTimestamp,
                    xValueFormatString: "DD.MM.YY HH:mm:ss.fff",
                    showInLegend: true,
                    dataPoints: feelings.map((snapshot) => {
                            return {
                                id: snapshot.snapshot_id,
                                x: new Date(snapshot.timestamp * 1000),
                                y: snapshot.feelings.happiness
                            }
                        }
                    )
                }]
        };

        let image;
        if (this.state.snapshot_id !== null) {
            image = <img alt="" height="400px"
                         src={"/users/" + this.props.user_id + "/snapshots/" + this.state.snapshot_id + "/color_image/data"}/>;
        } else {
            image = <div/>
        }

        return (
            <div>
                <Button onClick={this.playImages}>Play all Images</Button>
                <CanvasJSChart options={feelingsOptions}/>
                {image}
            </div>
        );
    }
}

export default UserCard;
