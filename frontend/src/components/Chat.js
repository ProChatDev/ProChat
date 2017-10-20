import React, { Component } from 'react';
//import Messages from './Messages';

export default class Chatbox extends Component {
  // constructor() {
  //   super();
  // }

  sendMessage = async (e) => {
    if (e.key === "Enter") {
      console.log(e)
      console.log("Works");
    }
  }

  render() {
    return (
      <div className="Chat">
        <input type="text" onKeyPress={this.props.sendMessage}></input>
      </div>
    );
  }
}