import React, { Component } from 'react';
import $ from 'jquery';

export default class Login extends Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);

    // Init state
    this.state = { message: '' };
  }

  // usernameChangeHandler(e) {
  //   this.setState({ username: e.target.value });
  // }

  handleSubmit(e) {
    e.preventDefault();

    const form_data = {};
    for (const field in this.refs)
      form_data[field] = this.refs[field].value;

    $.ajax({
      url: this.props.api_url + "/api/login",
      type: 'POST',
      data: {
        "username": form_data.username,
        "password": form_data.password
      },
      // headers: {
      //   'Access-Control-Allow-Origin': '*'
      // },
      // crossDomain: true, // Used to allow the post on the same host
      success: async (m) => {
        console.log(`Success: ${m}`);
      },
      error: async (err) => {
        console.log(`Error: ${JSON.stringify(err)}`);
        this.setState({ message: err.statusText });
      }
    });
  }

  render() {
    return (
      <div>
        <h3>{this.state.message}</h3>
        <form onSubmit={this.handleSubmit} className="login-form">
          <h1>Log In</h1>
          <input ref="username" className="username" type="text" name="username" placeholder="Enter username" />
          <br />
          <input ref="password" className="password" type="password" name="password" placeholder="Enter password" />
          <br />
          <button type="submit">Log In</button>
        </form>
      </div>
    );
  }
}