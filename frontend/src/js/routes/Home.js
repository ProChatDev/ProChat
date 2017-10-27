import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import Layout from '../components/Layout';
import Chat from '../components/chat/Chat';

export default class Home extends Component {
  isLoggedIn() {
    return (
      localStorage.getItem('email') &&
      localStorage.getItem('username') &&
      localStorage.getItem('id') &&
      localStorage.getItem('token')
    );
  }

  render() {
    if (!this.isLoggedIn()) {
      return (<Redirect to="/login" />);
    } else {
      return (
        <div>
          <Layout />
          <Chat />
        </div>
      );
    }
  }
}