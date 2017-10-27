import React, { Component } from 'react';
import Message from './Message';
import '../../../css/Chat.css';

export default class Messages extends Component {
  componentDidUpdate() {
    const msgList = document.getElementById('msg-list');
    msgList.scrollTop = msgList.scrollHeight;
  }

  render() {
    const messages = this.props.messages.map((m, i) => {
      return (
        <Message
          key={i}
          username={m.author.username}
          content={m.content}
          timestamp={m.timestamp}
          self={m.self}
        />
      );
    });

    return (
      <div className="messages" id="msg-list">
        {messages}
      </div>
    )
  }
}