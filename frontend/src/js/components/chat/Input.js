import React, { Component } from 'react';

export default class Input extends Component {
  constructor(props) {
    super(props);

    // Bind handle methods
    this.sendHandler = this.sendHandler.bind(this);
    this.inputHandler = this.inputHandler.bind(this);

    // Init state
    this.state = { input: '' };
  }

  sendHandler(e) {
    e.preventDefault();
    this.props.sendMessage(this.state.input);
    this.setState({ input: '' });
  }

  inputHandler(e) {
    this.setState({ input: e.target.value });
  }

  render() {
    return (
      <div className="container">
        <form className="chat-form" onSubmit={this.sendHandler}>
          <input
            type="text"
            placeholder="Send a message.."
            value={this.state.input}
            onChange={this.inputHandler}
            className="chat-input"
            disabled={this.props.disabled}
            id="chatinput"
            required
          />
        </form>
      </div>
    );
  }
}