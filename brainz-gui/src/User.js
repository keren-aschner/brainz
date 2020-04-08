import React from 'react';
import CanvasJSReact from "./canvasjs/canvasjs.react";

var CanvasJSChart = CanvasJSReact.CanvasJSChart;


class UserCard extends React.Component {
    constructor(props) {
        super(props);
        this.changeTimestamp = this.changeTimestamp.bind(this);
        this.state = {snapshot: null, feelings: []};
    }

    componentDidMount() {
        fetch("/users/" + this.props.user_id + "/feelings")
            .then(response => response.json())
            .then(data => this.setState({feelings: data}));
    }

    changeTimestamp(e) {
        this.setState({snapshot: e.dataPoint.id});
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
        return (
            <div>
                <CanvasJSChart options={feelingsOptions}/>
            </div>
        );
    }
}

export default UserCard;
