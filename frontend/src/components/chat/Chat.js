import React, { Component } from 'react';
import $ from 'jquery';
import Input from './Input';
import Messages from './Messages';
import '../../css/Chat.css';

export default class Chat extends Component {
  constructor(props) {
    super(props);

    // Init state
    this.state = { messages: [], inputDisabled: true };

    // Bind message methods
    this.sendMessage = this.sendMessage.bind(this);
    this.appendMessage = this.appendMessage.bind(this);

    // GET recent messages
    $.ajax({
      url: '/api/messages',
      type: 'GET',
      dataType: 'json',
      contentType: 'application/json',
      headers: {
        "Authorization": localStorage.getItem('token')
      },
      success: async (res) => {
        console.log(res);
        if (res.code === 200) {
          // Collect the last several messages for the page
          const messages = [];
          console.log(res.result);
          for (let i in res.result) {
            messages.push({
              username: res.result[i].username,
              content: res.result[i].content,
              timestamp: res.result[i].timestamp,
              id: res.result[i].id,
              author_id: res.result[i].sender_id
            });
          }
          // Set the state
          this.setState({
            messages: messages,
            inputDisabled: true
          });
        }
      }
    });

    // Connect to WebSocket via react proxy (not to be used in production build)
    this.socket = new WebSocket(`ws://${window.location.host}/gateway`);

    // On WebSocket open
    this.socket.onopen = async (e) => {
      console.log("WebSocket connection established.");
    }

    // On WebSocket close
    this.socket.onclose = async (e) => {
      console.log("WebSocket connection closed.");

      // Disable input, websocket closed
      const messages = this.state.messages;
      this.setState({
        messages: messages,
        inputDisabled: true
      });
    }

    // Listen for messages from WebSocket
    this.socket.onmessage = (e) => {
      console.log(`Message from WebSocket: ${e.data}`);
      let data = JSON.parse(e.data);
      switch (data.code) {
        // Successfully connected, send auth token
        case 1:
          this.socket.send(JSON.stringify({
            token: localStorage.getItem('token')
          }));
          break;
        // Successfully authenticated, unlock chatbox
        case 4:
          const messages = this.state.messages;
          this.setState({
            messages: messages,
            inputDisabled: false
          });
          break;
        default:
          break;
      }
      // Append message to page
      this.appendMessage({
        content: data.content,
        username: data.username,
        author_id: data.sender_id,
        timestamp: data.timestamp
      });
    }
  }

  /*
    The commented code I left in this method reminded me that we need to
    be able to compare the ID in localStorage to the ID returned from the
    websocket (or something like that) in order to style the client user's
    messages differently on the page. Keep this in mind when making changes.
  */

  // Send message to both WebSocket and state appending method
  sendMessage(message) {
    // Create the message object for the *client* to utilize
    // const msg = {
    //   username: localStorage.getItem('username'),
    //   content: message
    // }

    // The message was sent by the client user
    // Allows for different styling
    // msg.self = true;

    // Send message to Websocket
    this.socket.send(JSON.stringify({
      content: message
    }));
  }

  // Append message to state
  appendMessage(message) {
    const messages = this.state.messages;
    messages.push(message);
    this.setState({ messages, inputDisabled: false });
  }

  render() {
    return (
      <div className="chat-box">
        <Messages messages={this.state.messages} />
        <Input sendMessage={this.sendMessage} disabled={this.state.inputDisabled} />
      </div>
    );
  }
}