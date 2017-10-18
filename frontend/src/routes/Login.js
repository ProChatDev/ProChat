import React, { Component } from 'react';
import Layout from '../components/Layout';
import LoginForm from '../components/forms/LoginForm';

export default class Login extends Component {
  render() {
    return (
      <div>
        <Layout active_link={this.props.children} />
        <LoginForm />
      </div>
    );
  }
}