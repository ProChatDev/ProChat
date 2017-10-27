import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import Layout from '../components/Layout';
import LoginForm from '../components/forms/LoginForm';

export default class Login extends Component {
  isLoggedIn() {
    return (
      localStorage.getItem('email') &&
      localStorage.getItem('username') &&
      localStorage.getItem('id') &&
      localStorage.getItem('token')
    );
  }

  render() {
    if (this.isLoggedIn()) {
      return (<Redirect to="/" />);
    } else {
      return (
        <div>
          <Layout active_link={this.props.children} />
          <LoginForm />
        </div>
      );
    }
  }
}