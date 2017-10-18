import React, { Component } from 'react';
import $ from 'jquery';

export default class RegistrationForm extends Component {
  constructor(props) {
    super(props);

    // Bind registration handle method
    this.handleSubmit = this.handleSubmit.bind(this);

    // Init state
    this.state = { message: '' };
  }

  // Registration handle
  handleSubmit(e) {
    e.preventDefault();

    // Collect data from the form
    const form_data = {};
    for (const field in this.refs)
      form_data[field] = this.refs[field].value;

    $.ajax({
      url: '/api/register',
      type: 'POST',
      data: JSON.stringify({
        email: form_data.email,
        username: form_data.username,
        password: form_data.password
      }),
      dataType: 'json',
      contentType: 'application/json',
      success: async (res) => {
        console.log(JSON.stringify(res));
        switch (res.code) {
          case 400:
            this.setState({ message: `${res.message}` });
            this.refs.username.value = "";
            this.refs.password.value = "";
            break;
          case 409:
            this.setState({ message: "A user with this email or username already exists." });
            this.refs.email.value = "";
            this.refs.username.value = "";
            this.refs.password.value = "";
            break;
          default:
            for (const key in res)
              localStorage.setItem(key, res[key]);
        }
      }
    });
  }

  render() {
    return (
      <div>
        <h3>{this.state.message}</h3>
        <form onSubmit={this.handleSubmit} className="registration-form">
          <h3>Register</h3>
          <input
            className="email"
            name="email"
            type="email"
            ref="email"
            placeholder="Email"
          />
          <br />
          <input
            className="username"
            name="username"
            type="text"
            ref="username"
            placeholder="Username"
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
          <button type="submit">Register</button>
        </form>
      </div>
    );
  }
}