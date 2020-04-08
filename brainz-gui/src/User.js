import React from 'react';
import CanvasJSReact from "./canvasjs/canvasjs.react";

var CanvasJSChart = CanvasJSReact.CanvasJSChart;


class UserCard extends React.Component {
    constructor(props) {
        super(props);
        this.changeTimestamp = this.changeTimestamp.bind(this);
        this.state = {snapshot: null};
    }

    changeTimestamp(e) {
        this.setState({snapshot: e.dataPoint.id});
    }

    render() {
        const feelings = [
            {
                id: 1, timestamp: 1575446887.339, feelings: {hunger: -1, thirst: -0.5, exhaustion: 0, happiness: 0}
            }, {
                id: 2, timestamp: 1575446890.339, feelings: {hunger: 0.5, thirst: 0.2, exhaustion: -0.5, happiness: 0.1}
            }, {
                id: 3, timestamp: 1575446892.2, feelings: {hunger: 0.5, thirst: 0.35, exhaustion: 0.1, happiness: 0.75}
            },
            {
                id: 4, timestamp: 1575446892.9, feelings: {hunger: 0.7, thirst: 0.37, exhaustion: 0.5, happiness: 1}
            }];

        const options = {
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
                                id: snapshot.id,
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
                                id: snapshot.id,
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
                                id: snapshot.id,
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
                                id: snapshot.id,
                                x: new Date(snapshot.timestamp * 1000),
                                y: snapshot.feelings.happiness
                            }
                        }
                    )
                }]
        };
        return (
            <div>
                <CanvasJSChart options={options}/>
            </div>
        );
    }
}

export default UserCard;
