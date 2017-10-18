import React, { Component } from 'react';
import Layout from '../components/Layout';
import RegistrationForm from '../components/forms/RegistrationForm';

export default class Register extends Component {
  render() {
    return (
      <div>
        <Layout active_link={this.props.children} />
        <RegistrationForm />
      </div>
    );
  }
}