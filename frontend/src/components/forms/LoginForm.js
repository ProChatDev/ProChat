import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import $ from 'jquery';

export default class LoginForm extends Component {
  constructor(props) {
    super(props);

    // Bind login handle method
    this.handleSubmit = this.handleSubmit.bind(this);

    // Init state
    this.state = { message: '', redirect: false };
  }

  // Login handle
  handleSubmit(e) {
    e.preventDefault();

    // Collect data from the form
    const form_data = {};
    for (const field in this.refs)
      form_data[field] = this.refs[field].value;

    $.ajax({
      url: '/api/login',
      type: 'POST',
      data: JSON.stringify({
        username: form_data.username,
        password: form_data.password
      }),
      dataType: 'json',
      contentType: 'application/json',
      success: async (res) => {
        switch (res.code) {
          case 400:
            this.setState({ message: `${res.message}` });
            this.refs.username.value = "";
            this.refs.password.value = "";
            break;
          case 403:
            this.setState({ message: "Your username or password was incorrect." });
            this.refs.username.value = "";
            this.refs.password.value = "";
            break;
          default:
            for (const key in res)
              localStorage.setItem(key, res[key]);
            this.setState({ redirect: true });
        }
      }
    });
  }

  render() {
    const { redirect } = this.state;

    return (
      <div>
        <h3 style={{ textAlign: 'center' }}>{this.state.message}</h3>
        <form onSubmit={this.handleSubmit} className="login-form">
          <h3>Log In</h3>
          <input
            className="username"
            name="username"
            type="text"
            ref="username"
            placeholder="Username/Email"
          />
          <br />
          <input
            className="password"
            name="password"
            type="password"
            ref="password"
            placeholder="Password"
          />
          <br />
          <button type="submit">Log In</button>
        </form>
        {redirect && (<Redirect to="/" />)}
      </div>
    );
  }
}