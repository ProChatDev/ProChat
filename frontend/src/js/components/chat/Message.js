import React, { Component } from 'react';

export default class Messages extends Component {
  render() {
    const msgSelf = this.props.self ? 'msg-self' : '';
    const msgDate = new Date(this.props.timestamp).toLocaleTimeString();

    return (
      <div className={`msg ${msgSelf}`}>
        <span className="msg-username">{ this.props.username }</span>
        <span className="msg-timestamp">{msgDate}</span>
        <div className="msg-content" style={{wordWrap: 'break-word'}}>{ this.props.content }</div>
      </div>
    );
  }
}