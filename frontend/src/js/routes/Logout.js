import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import Layout from '../components/Layout';

export default class Logout extends Component {
  render() {
    localStorage.clear();
    return (
      <div>
        <Layout active_link={this.props.children} />
        <Redirect from="/logout" to="/" />
      </div>
    );
  }
}