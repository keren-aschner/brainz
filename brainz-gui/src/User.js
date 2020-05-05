import React from 'react';
import CanvasJSReact from "./canvasjs/canvasjs.react";
import {Button, Card, Col, Row} from 'antd';
import {PauseCircleOutlined, PlayCircleOutlined, StepBackwardOutlined} from '@ant-design/icons'
import {format} from "date-fns";

let CanvasJSChart = CanvasJSReact.CanvasJSChart;


class User extends React.Component {
    constructor(props) {
        super(props);
        this.changeImage = this.changeImage.bind(this);
        this.restartImages = this.restartImages.bind(this);
        this.playImages = this.playImages.bind(this);
        this.stopImages = this.stopImages.bind(this);
        this.state = {snapshot: 0, snapshot_id: null, snapshot_date: null, playing: false, feelings: [], snapshots: []};
    }

    static getDerivedStateFromProps(props, state) {
        return {user_id: props.user_id};
    }

    componentDidMount() {
        this.fetch_user_data(this.state.user_id);
    }

    getSnapshotBeforeUpdate(prevProps, prevState) {
        this.prev_user = prevState.user_id;
        return null;
    }

    componentDidUpdate() {
        let user_id = this.state.user_id;

        if (this.prev_user !== user_id) {
            clearInterval(this.timerID);
            this.fetch_user_data(user_id);
            this.setState({
                snapshot: 0,
                snapshot_id: null,
                snapshot_date: null,
                playing: false
            });
        }
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    fetch_user_data(user_id) {
        fetch(`${window.api_server}/users/${user_id}/feelings`)
            .then(response => response.json())
            .then(data => this.setState({feelings: data}));

        fetch(`${window.api_server}/users/${user_id}/snapshots`)
            .then(response => response.json())
            .then(data => this.setState({snapshots: data}));
    }

    changeImage(e) {
        if (!this.state.playing) {
            this.setState({
                snapshot_id: e.dataPoint.id,
                snapshot_date: e.dataPoint.x
            });
        }
    }

    restartImages(e) {
        this.setState(state => ({
            snapshot: 0,
            snapshot_id: state.snapshots[0].snapshot_id,
            snapshot_date: new Date(state.snapshots[0].timestamp * 1000)
        }));
    }

    playImages(e) {
        if (!this.state.playing) {
            this.setState({
                playing: true
            });
            this.timerID = setInterval(
                () => this.tick(),
                250
            );
        }
    }

    stopImages(e) {
        clearInterval(this.timerID);
        this.setState({playing: false});
    }

    tick() {
        let snapshotsSize = this.state.snapshots.length - 1;
        if (this.state.snapshot === snapshotsSize) {
            clearInterval(this.timerID);
            this.setState({
                snapshot: 0,
                playing: false
            });
            return;
        }

        this.setState(state => ({
            snapshot: state.snapshot + 1,
            snapshot_id: state.snapshots[state.snapshot + 1].snapshot_id,
            snapshot_date: new Date(state.snapshots[state.snapshot + 1].timestamp * 1000)
        }));
    }

    render() {
        let feelings = this.state.feelings;

        const feelingsOptions = {
            theme: "light2",
            backgroundColor: "#f5f5f5",
            height: 500,
            zoomEnabled: true,
            animationEnabled: true,
            title: {
                text: "Feelings over time"
            },
            axisY: {
                title: "Feelings",
            },
            axisX: {
                title: "timestamp",
                valueFormatString: "DD.MM.YY HH:mm:ss",
                labelFontSize: 14
            },
            toolTip: {
                shared: true
            },
            data: [
                {
                    type: "spline",
                    name: "hunger",
                    mousemove: this.changeImage,
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
                    mousemove: this.changeImage,
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
                    mousemove: this.changeImage,
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
                    mousemove: this.changeImage,
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
        let date;
        if (this.state.snapshot_id !== null) {
            date = format(this.state.snapshot_date, "dd.MM.yy HH:mm:ss");
            image = <img
                alt="" style={{maxWidth: "100%", marginTop: 80}}
                src={`${window.api_server}/users/${this.state.user_id}/snapshots/${this.state.snapshot_id}/color_image/data`}
            />
        } else {
            date = <div/>
            image = <span style={{height: 330}}/>
        }

        return (
            <div>
                <Row style={{margin: 40}}>
                    <Col span={1}/>
                    <Col span={15}>
                        <CanvasJSChart options={feelingsOptions}/>
                    </Col>
                    <Col span={1}/>
                    <Col span={6}>
                        <Card style={{background: '#fafafa'}}
                              actions={[
                                  <Button style={{margin: 16}} type="link" onClick={this.restartImages}>
                                      <StepBackwardOutlined style={{fontSize: 25}}/>
                                  </Button>,
                                  <Button style={{margin: 16}} type="link" onClick={this.playImages}>
                                      <PlayCircleOutlined style={{fontSize: 25}}/>
                                  </Button>,
                                  <Button style={{margin: 16}} type="link" onClick={this.stopImages}>
                                      <PauseCircleOutlined style={{fontSize: 25}}/>
                                  </Button>]}
                              cover={image}>
                            <Card.Meta description={date} style={{textAlign: 'center'}}/>
                        </Card>
                    </Col>
                    <Col span={1}/>
                </Row>
            </div>
        );
    }
}

export default User;
